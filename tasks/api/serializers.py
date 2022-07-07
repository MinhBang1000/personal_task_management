from tasks.models import Task,Priority, Status
from rest_framework import serializers
from status.api.serializers import StatusSerializer
from priorities.api.serializers import PrioritySerializer 

class TaskSerializer(serializers.ModelSerializer):

    priority_id = serializers.PrimaryKeyRelatedField(
        queryset=Priority.objects.all(), source="priority", write_only=True
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source="status", write_only=True
    )
    status = StatusSerializer(read_only=True)
    priority = PrioritySerializer(read_only=True)


    class Meta:
        model=Task
        fields=[
            "id",
            "priority",
            "priority_id",
            "status",
            "status_id",
            "task_name",
            "description",
            "due_date",
            "created"
        ]