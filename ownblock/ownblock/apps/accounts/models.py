from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from model_utils import Choices


from apps.buildings.models import Apartment, Building


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

    def create_superuser(self, email, first_name, last_name, password):
        return self.create_user(email, first_name,
                                last_name, password, role='admin')


class User(AbstractBaseUser):

    ROLES = Choices('resident', 'manager', 'admin')

    email = models.EmailField(unique=True, max_length=160)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    apartment = models.ForeignKey(Apartment, null=True, blank=True)
    buildings = models.ManyToManyField(Building, blank=True)

    role = models.CharField(choices=ROLES, default='resident')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'role')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    # Django admin hooks

    @property
    def is_staff(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
