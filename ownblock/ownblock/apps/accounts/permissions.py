from rest_framework.permissions import IsAuthenticated


class IsResident(IsAuthenticated):

    """User must be associated with an apartment"""

    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                request.user.apartment_id is not None)


class IsManager(IsAuthenticated):

    """User must have manager role"""

    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                request.user.role == 'manager')
