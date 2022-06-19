from pyexpat import model
from rest_framework import serializers, permissions
from workspaces.models import Workspace

class WorkspaceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        exclude=["owner", "image"]

class WorkspaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        fields="__all__"