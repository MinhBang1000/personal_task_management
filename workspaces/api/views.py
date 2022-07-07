from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import WorkspaceSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from workspaces.models import Workspace
from formats.formats import success, error
# Create your views here.
class WorkspaceViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = WorkspaceSerializer
    
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        owner = self.request.user 
        return serializer.save(owner=owner)

    def update(self, request, *args, **kwargs):
        kwargs["partial"]=True
        return super().update(request, *args, **kwargs)


    