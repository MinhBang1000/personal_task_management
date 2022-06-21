from asyncio import tasks
from pyexpat import model
from rest_framework import serializers, permissions
from tasks.models import Task
from workspaces.models import Workspace

class WorkspaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        fields=["image"]

class WorkspaceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Workspace
        exclude=["owner", "image"]        

class WorkspaceListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Workspace
        exclude=["owner"]
    # Only all fields of Workspace model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=["id", "task_name"]
    # This serializer is used below

class WorkspaceDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(read_only=True, many=True)
    class Meta:
        model=Workspace
        exclude=["owner"]
    # Get with all tasks