from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    _user_has_perm,
)


from model_utils import Choices


from apps.organizations.models import Organization
from apps.buildings.models import Apartment


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, role, password=None):

        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role, password):
        return self.create_user(email, first_name,
                                last_name,
                                role=role,
                                password=password,
                                is_staff=True)


class User(AbstractBaseUser):

    ROLES = Choices('resident', 'manager')

    email = models.EmailField(unique=True, max_length=160)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    organization = models.ForeignKey(Organization, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)

    role = models.CharField(choices=ROLES, default='resident', max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    MODEL_PERMISSIONS = {
        'resident': {
            'notices.add_notice',
        },
        'manager': {
            'notices.add_notice',
        },
    }

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    # Hook for custom auth backend

    def has_model_permissions(self, perm):
        """Provides model-scpe permissions"""
        return perm in self.MODEL_PERMISSIONS.get(self.role, {})

    # Hooks for Django admin and Rest Framework

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, module):
        return self.is_staff
