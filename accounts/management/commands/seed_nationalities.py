# accounts/management/commands/seed_nationalities.py
from django.core.management.base import BaseCommand
from accounts.models import Nationality
from faker import Faker

class Command(BaseCommand):
    help = "Seed the Nationality table with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        nationalities = set()
        for _ in range(20):  # Generate 20 unique nationalities
            nationalities.add(fake.country())
        for name in nationalities:
            Nationality.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Successfully seeded nationalities."))