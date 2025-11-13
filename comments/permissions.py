from rest_framework import permissions

class CanAccessComments(permissions.BasePermission):

    def has_permission(self, request, view):
        #only auth user with role moderator can access
        return request.user.is_authenticated and request.user.role == "moderator"
