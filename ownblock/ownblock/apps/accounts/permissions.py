from rest_framework import permissions


class IsResidentOrManager(permissions.IsAuthenticated):

    """Must have resident/manager role and be connected
    to a building"""

    def has_permission(self, request, view):

        return (super().has_permission(request, view) and
                request.user.role in ('resident', 'manager') and
                request.building is not None)


class IsResidentOrManagerReadOnly(IsResidentOrManager):

    """
    Only manager has writer permissions
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'manager'
