# python
from rest_framework import serializers
from .models import Category, Tag, Task, Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'task']
        read_only_fields = ['id', 'created_at', 'task']  # task will be set from URL

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