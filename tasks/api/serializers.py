from asyncio import tasks
from tasks.models import Task
from rest_framework import serializers

class TaskReadSerializer(serializers.ModelSerializer):
    workspace = serializers.StringRelatedField()
    priority = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    class Meta:
        model=Task
        fields="__all__"
        depth=1

class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        exclude=["workspace"]

class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields=[
            "task_name",
            "description",
            "due_date",
            "priority"
        ]

class TaskUpdateStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields=[
            "status"
        ]