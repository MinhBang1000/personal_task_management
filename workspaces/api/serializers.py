from pyexpat import model
from rest_framework import serializers, permissions
from workspaces.models import Workspace

class WorkspaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        exclude=["owner", "title", "description"]

    def update(self, instance, validated_data):
        instance.image = validated_data["image"] 
        instance.save()
        return instance

class WorkspaceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Workspace
        exclude=["owner", "image"]        

class WorkspaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Workspace
        fields="__all__"