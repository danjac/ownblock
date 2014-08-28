from rest_framework import permissions


class HasRole(permissions.BasePermission):
    role = None

    def has_permission(self, request, view):
        return (request.user.is_authenticated() and
                request.user.role == self.role)


class IsManager(HasRole):
    role = 'manager'


class IsResident(HasRole):
    role = 'resident'
