from rest_framework.permissions import BasePermission

class IsModeratororSelf(BasePermission):
    "mods have access to everything and normal users can only access themselves"

    def has_object_permission(self, request, view, obj):
        if request.user.role == "moderator":
            return True
        if request.user.role == "user":
            return obj == request.user