from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate


class Command(BaseCommand):
    help = "Test authentication by email and username"

    def handle(self, *args, **options):
        User = get_user_model()
        email = "user@example.com"
        username = "user1"
        password = "pass1234"

        # Ensure a clean start
        User.objects.filter(email=email).delete()
        User.objects.filter(username=username).delete()

        user = User.objects.create_user(email=email, username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created user id={user.id} email={user.email} username={user.username}"))

        u1 = authenticate(username=email, password=password)
        self.stdout.write("Auth by email: {}".format("OK" if u1 is not None else "FAIL"))

        u2 = authenticate(username=username, password=password)
        self.stdout.write("Auth by username: {}".format("OK" if u2 is not None else "FAIL"))
