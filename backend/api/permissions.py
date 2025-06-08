from rest_framework.permissions import BasePermission


class AllowAny(BasePermission):
    """
    Allows access to all
    """

    def has_permission(self, request, view):
        return True
