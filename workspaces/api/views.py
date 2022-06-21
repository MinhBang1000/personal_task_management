from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import WorkspaceCreateSerializer, WorkspaceUpdateSerializer, WorkspaceListSerializer, WorkspaceDetailSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from workspaces.models import Workspace
from formats.formats import success, error
# Create your views here.
class WorkspaceViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.action == "retrieve":
                return WorkspaceDetailSerializer
            return WorkspaceListSerializer
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
        workspace_serializer = WorkspaceListSerializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=success(data=workspace_serializer.data, code=201, message="Create Workspace Successful!"), status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        read_serializer = WorkspaceListSerializer(instance)
        return Response(data=success(data=read_serializer.data, code=200, message="Update Workspace Successful!"), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="List User's Workspaces Successful!")
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = WorkspaceDetailSerializer(instance)
        data = success(data=serializer.data, code=200, message="Retrieve Workspace Succesful!")
        return Response(data=data, status=status.HTTP_200_OK)

    