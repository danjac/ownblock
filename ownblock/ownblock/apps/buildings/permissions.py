from rest_framework.permissions import BasePermission


class IsBuilding(BasePermission):

    """Checks if a current building (preselected by middleware)
    has been assigned for this user"""

    def has_permission(self, request, view):
        return request.building is not None
