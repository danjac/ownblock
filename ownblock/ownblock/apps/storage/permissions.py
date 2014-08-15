from apps.accounts.permissions import IsResidentOrManager


class IsOwnerOrManager(IsResidentOrManager):

    def has_object_permission(self, request, view, obj):
        return obj.can_edit_or_delete(request.user)
