from rest_framework.permissions import IsAuthenticated


class IsResidentOrManager(IsAuthenticated):

    def has_permission(self, request, view):

        return (super().has_permission(request, view) and
                request.building is not None)
