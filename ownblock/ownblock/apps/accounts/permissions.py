from rest_framework.permissions import IsAuthenticated


class IsResidentOrManager(IsAuthenticated):

    """Must have resident/manager role and be connected
    to a building"""

    def has_permission(self, request, view):

        return (super().has_permission(request, view) and
                request.user.role in ('resident', 'manager') and
                request.building is not None)
