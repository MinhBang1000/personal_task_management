from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, filters
from workspaces.models import Workspace
from rest_framework.response import Response
from tasks.models import Task
from .serializers import TaskSerializer
from tasks.api import permissions as custom_permissions

# Create your views here.
class TaskViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated, custom_permissions.IsOwnerTask]
    filterset_fields=["status__name","due_date"]
    filter_backends=[filters.SearchFilter]
    search_fields = ['task_name']
    serializer_class = TaskSerializer

    def get_queryset(self):
        workspace_id = self.kwargs["workspace_id"]
        return Task.objects.filter(workspace=workspace_id).select_related()

    def perform_create(self, serializer):
        try:
            instance = Workspace.objects.get(id=self.kwargs["workspace_id"])
        except:
            ValidationError("You don't have this workspace!")
        serializer.save(workspace=instance)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True) # Partial edit
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)