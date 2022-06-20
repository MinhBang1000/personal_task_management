from django.db import models
from workspaces.models import Workspace

# Create your models here.

class Priority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Task(models.Model):
    task_name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    due_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="tasks")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="tasks")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.task_name