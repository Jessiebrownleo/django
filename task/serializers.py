from rest_framework import serializers
from .models import Category, Tag, Task

class CategorySerializer(serializers.ModelSerializer):
        task_count = serializers.IntegerField(read_only=True)
        status = serializers.SerializerMethodField()

        class Meta:
            model = Category
            fields = ['id', 'name', 'hex_color', 'task_count', 'status']

        def get_status(self, obj):
            if obj.task_count == 0:
                return "none"
            elif obj.task_count < 3:
                return "a few"
            else:
                return "too many"

    # Option Three
class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ['id', 'title',
                      'description', 'status',
                      'category',
                      'created_at', 'updated_at',
                      'tags']
class TagSerializer(serializers.ModelSerializer):
        task_count = serializers.IntegerField(read_only=True)
        status = serializers.SerializerMethodField()

        class Meta:
            model = Tag
            fields = ['id', 'name', 'task_count', 'status']

        def get_status(self, obj):
            if obj.task_count == 0:
                return "none"
            elif obj.task_count < 3:
                return "a few"
            else:
                return "too many"