from django.forms import ValidationError
from rest_framework import permissions
from workspaces.models import Workspace

class IsOwnerTask(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            owner = Workspace.objects.get(id=view.kwargs["workspace_id"]).owner
        except:
            return False
        return request.user.id == owner.id