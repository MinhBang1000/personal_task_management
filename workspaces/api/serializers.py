from asyncio import tasks
from pyexpat import model
from rest_framework import serializers, permissions
from tasks.models import Task
from workspaces.models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        fields=[
            "id",
            "title",
            "description",
            "image",
            "created"
        ]
        read_only_fields = ["created"]