# python
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Tag, Task, Note
from .serializers import CategorySerializer, TagSerializer, TaskSerializer, NoteSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # GET /task/{id}/notes — list notes for a task
    # POST /task/{id}/notes — create note for a task
    @action(detail=True, methods=['get', 'post'], url_path='notes')
    def notes(self, request, pk=None):
        task = self.get_object()

        if request.method.lower() == 'get':
            qs = task.notes.order_by('-created_at')
            serializer = NoteSerializer(qs, many=True)
            return Response(serializer.data)

        # POST
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # set task from URL
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /task/{id}/notes/{note_id} — retrieve single note
    # PUT/PATCH /task/{id}/notes/{note_id} — update note
    # DELETE /task/{id}/notes/{note_id} — delete note
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path=r'notes/(?P<note_id>[^/.]+)')
    def note_detail(self, request, pk=None, note_id=None):
        task = self.get_object()
        try:
            note = task.notes.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method.lower() == 'get':
            return Response(NoteSerializer(note).data)

        if request.method.lower() in ['put', 'patch']:
            partial = request.method.lower() == 'patch'
            serializer = NoteSerializer(note, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save(task=task)  # keep task bound
            return Response(serializer.data)

        # DELETE
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        task_count=Count('tasks')
    )
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.annotate(
        task_count=Count('tasks')
    )
    serializer_class = TagSerializer