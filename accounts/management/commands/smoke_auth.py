import json
import sys
import uuid
from django.core.management.base import BaseCommand
from rest_framework.test import APIClient


class Command(BaseCommand):
    help = "Smoke test for authentication endpoints: register, login, user, refresh, verify"

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default="",
            help="Optional base URL prefix if running against an external server (leave empty for in-process test client)",
        )
        parser.add_argument(
            "--password",
            default="Passw0rd!",
            help="Password to use for the test user (default: Passw0rd!)",
        )

    def handle(self, *args, **options):
        base = options["base_url"].rstrip("/")
        password = options["password"]
        client = APIClient()

        # Create unique user data per run
        uniq = uuid.uuid4().hex[:8]
        email = f"test_{uniq}@example.com"
        username = f"user_{uniq}"
        first_name = "Test"
        last_name = "User"

        def url(path: str) -> str:
            return f"{base}{path}" if base else path

        def log_result(step: str, ok: bool, resp):
            status = getattr(resp, "status_code", None)
            try:
                data = resp.json() if hasattr(resp, "json") else json.loads(resp.content.decode())
            except Exception:
                data = getattr(resp, "data", None)
            self.stdout.write((self.style.SUCCESS if ok else self.style.ERROR)(f"{step}: {'OK' if ok else 'FAIL'} (status={status})"))
            if not ok:
                self.stdout.write(self.style.WARNING(f"Response: {data}"))

        # 1) Register
        register_payload = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "re_password": password,
        }
        resp = client.post(url("/auth/register/"), register_payload, format="json")
        ok = 200 <= resp.status_code < 300
        log_result("Register", ok, resp)
        if not ok:
            sys.exit(1)

        # 2) Login
        login_payload = {"email": email, "password": password}
        resp = client.post(url("/auth/login/"), login_payload, format="json")
        ok = resp.status_code == 200 and "access" in resp.json() and "refresh" in resp.json()
        log_result("Login", ok, resp)
        if not ok:
            sys.exit(1)
        tokens = resp.json()
        access = tokens["access"]
        refresh = tokens["refresh"]

        # 3) Get current user
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        resp = client.get(url("/auth/user/"))
        ok = resp.status_code == 200 and resp.json().get("email") == email
        log_result("Get current user", ok, resp)
        if not ok:
            sys.exit(1)

        # 4) Refresh token
        client.credentials()  # clear auth for refresh
        resp = client.post(url("/auth/refresh/"), {"refresh": refresh}, format="json")
        ok = resp.status_code == 200 and "access" in resp.json()
        log_result("Refresh", ok, resp)
        if not ok:
            sys.exit(1)
        new_access = resp.json()["access"]

        # 5) Verify tokens (access and refresh)
        resp = client.post(url("/auth/verify/"), {"token": new_access}, format="json")
        ok = resp.status_code == 200
        log_result("Verify new access", ok, resp)
        if not ok:
            sys.exit(1)

        resp = client.post(url("/auth/verify/"), {"token": refresh}, format="json")
        ok = resp.status_code == 200
        log_result("Verify refresh", ok, resp)
        if not ok:
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("All auth endpoint smoke tests passed."))
