from rest_framework import permissions

class CanAccessComments(permissions.BasePermission):
    """
    Allows access only to users who have the correct role.
    """

    def has_permission(self, request, view):
        # Only authenticated users with role 'admin' can access
        return request.user.is_authenticated and request.user.role == "moderator"
