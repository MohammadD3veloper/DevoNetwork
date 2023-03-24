from rest_framework import permissions


class IsGroupAdminOrAuthenticated(permissions.BasePermission):
    """ Check user permissions for update/delete """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS and \
            request.user.is_authenticated:
            return True

        if obj.admin == request.user:
            return True
