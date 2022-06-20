from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import WorkspaceCreateSerializer, WorkspaceUpdateSerializer,WorkspaceReadSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from workspaces.models import Workspace
# Create your views here.
class WorkspaceViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkspaceReadSerializer
        else:
            if self.request.method == "PUT":
                return WorkspaceUpdateSerializer
        return WorkspaceCreateSerializer

    def perform_create(self, serializer):
        owner = self.request.user 
        return serializer.save(owner=owner)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        workspace_serializer = WorkspaceReadSerializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=workspace_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        read_serializer = WorkspaceReadSerializer(instance)
        return Response(data=read_serializer.data, status=status.HTTP_200_OK)

