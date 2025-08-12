
from django.contrib import admin
from .models import Category, Tag, Task, Note

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1
    fields = ('content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'is_completed', 'due_date', 'created_at')
    list_filter = ('status', 'is_completed', 'category', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    inlines = [NoteInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hex_color')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'task')