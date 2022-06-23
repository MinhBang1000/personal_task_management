from django.forms import ValidationError
from requests import delete
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions,status, filters
from rest_framework.response import Response
from workspaces.models import Workspace
from tasks.models import Task
from .serializers import TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskUpdateStatusSerializer
from tasks.api import permissions as custom_permissions
from rest_framework.decorators import api_view, permission_classes
from formats.formats import success, error

# Create your views here.
class TaskViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated, custom_permissions.IsOwnerTask]
    filterset_fields=["status__name","created","due_date"]
    # filter_backends=[filters.SearchFilter]
    # search_fields = ['task_name']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskReadSerializer
        else:
            if self.request.method == "PUT":
                if self.request.data.get("status"):
                    return TaskUpdateStatusSerializer
                return TaskUpdateSerializer
        return TaskCreateSerializer 

    def get_queryset(self):
        workspace_id = self.kwargs["workspace_id"]
        return Task.objects.filter(workspace=workspace_id)

    def perform_create(self, serializer):
        try:
            instance = Workspace.objects.get(id=self.kwargs["workspace_id"])
        except:
            ValidationError("You don't have this workspace!")
        return serializer.save(workspace=instance)

    def perform_update(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        read_serializer = TaskReadSerializer(instance)
        return Response(data=success(data=read_serializer.data, code=200, message="Create Task Successful!"), status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="List Task Successful!")
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="Retrieve Task Successful!")
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(data=success(data=None, code=204, message="Remove Task Successful!"),status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        read_serializer = TaskReadSerializer(instance)
        return Response(data=success(data=read_serializer.data, code=200, message="Update Task Successful!"), status=status.HTTP_200_OK)