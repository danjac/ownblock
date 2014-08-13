from rest_framework import permissions

from apps.accounts.permissions import IsResidentOrManager


class IsBookingResidentOrManager(IsResidentOrManager):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.role == 'manager' or
                obj.resident_id == request.user.id)
