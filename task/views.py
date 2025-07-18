from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from .models import Category, Tag, Task
from .serializers import CategorySerializer, TagSerializer, TaskSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        task_count = Count('tasks')  # Count distinct tasks in each category
    )
    serializer_class = CategorySerializer
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.annotate(
        task_count=Count('tasks')  # Count related tasks
    )
    serializer_class = TagSerializer