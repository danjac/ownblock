from rest_framework import permissions

from apps.accounts.permissions import IsResidentOrManager


class IsBookingResidentOrManager(IsResidentOrManager):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return (self.request.user.role == 'manager' or
                obj.resident_id == self.request.user.id)
