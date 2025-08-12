
from django.db import models

class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Link each note to a task
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.content

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_color = models.CharField(max_length=50, null=True)  # Default to white

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS = [
        ('INIT', 'Init'),
        ('in_progress', 'In Progress'),
        ('CANCLE', 'Cancle'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tasks")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='INIT')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title