from django.core.management.base import BaseCommand
from faker import Faker
import random

from task.models import Category, Tag, Task

class Command(BaseCommand):
    help = 'Seed the database with fake Categories, Tags, and Tasks'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data (optional)
        Task.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.unique.word().capitalize(),
                hex_color=fake.hex_color()
            )
            categories.append(category)

        # Create Tags
        tags = []
        for _ in range(10):
            tag = Tag.objects.create(name=fake.unique.word())
            tags.append(tag)

        # Create Tasks
        for _ in range(50):
            task = Task.objects.create(
                title=fake.sentence(nb_words=6),
                description=fake.paragraph(),
                category=random.choice(categories),
                is_completed=fake.boolean(chance_of_getting_true=30),
                due_date=fake.date_between(start_date='-30d', end_date='+30d'),
                status=random.choice(['INIT', 'in_progress', 'CANCEL']),
            )
            selected_tags = random.sample(tags, k=random.randint(0, 3))
            task.tags.set(selected_tags)

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded the database!'))
