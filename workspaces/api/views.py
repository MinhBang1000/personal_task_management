from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import WorkspaceWriteSerializer, WorkspaceReadSerializer
from rest_framework import permissions
from workspaces.models import Workspace
# Create your views here.
class WorkspaceViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    queryset=Workspace.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkspaceReadSerializer
        return WorkspaceWriteSerializer

    def perform_create(self, serializer):
        owner = self.request.user 
        image = self.request.data["image"]
        serializer.save(owner=owner, image=image)

