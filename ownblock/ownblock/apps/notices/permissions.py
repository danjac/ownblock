from rest_framework import permissions

from apps.accounts.permissions import IsResidentOrManager


class IsAuthorOrManager(IsResidentOrManager):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.can_edit_or_delete(request.user)
