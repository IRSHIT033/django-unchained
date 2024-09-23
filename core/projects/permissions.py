from rest_framework import permissions
from .models import Project

class IsOwnerOrContributor(permissions.BasePermission):
    """
    Custom permission to only allow owners or contributors to view/edit the project.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the project
        if request.user == obj.owner:
            return True
        # Check if the user is a contributor to the project
        if request.user in obj.contributors.all():
            return True
        return False

