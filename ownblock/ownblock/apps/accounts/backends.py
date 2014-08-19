from django.contrib.auth.backends import ModelBackend


class ObjectPermissionBackend(ModelBackend):

    """Provides a logic-based backend for row- and model-level
    permissions without requiring additional database models.

    The user class must implement has_model_permissions. Individual models
    should implement has_permission(user, perm) or will be skipped.

    By default:
    - staff always returns True
    - anonymous/inactive users are always False
    """

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous():
            return False
        if user_obj.is_staff:
            return True
        if obj is None:
            if not hasattr(user_obj, 'has_model_permission'):
                raise AttributeError(
                    'User model must implement has_model_permission')
            return user_obj.has_model_permission(perm)
        if not hasattr(obj, 'has_permission'):
            return False
        return obj.has_permission(user_obj, perm)
