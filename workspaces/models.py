from django.db import models
from users.models import User

# Create your models here.
class Workspace(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaces")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
