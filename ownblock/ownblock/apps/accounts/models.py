from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)

from guardian.shortcuts import assign_perm

from model_utils import Choices, FieldTracker


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
                                is_staff=True,
                                is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):

    ROLES = Choices('resident', 'manager')

    email = models.EmailField(unique=True, max_length=160)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    organization = models.ForeignKey(Organization, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)

    role = models.CharField(choices=ROLES, default='resident', max_length=10)

    tracker = FieldTracker(fields=('role', 'organization'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    def save(self, **kwargs):
        has_changed = bool(self.tracker.changed())

        super().save(**kwargs)

        assign_perm('accounts.change_user', self, self)

        if not has_changed:
            return

        self.groups.clear()

        if self.role == 'residents':
            self.groups.add(create_residents_group())

        if self.role == 'manager':
            self.groups.add(create_managers_group())

            if self.organization:
                self.groups.add(self.organization.group)


def _create_group(name, models):
    group, created = Group.objects.get_or_create(name=name)
    if not created:
        return group

    permissions = ('add', 'change', 'delete')

    for app_label, model in models:
        for perm in permissions:
            assign_perm('%s.%s_%s' % (app_label, perm, model), group)

    return group


def create_managers_group():
    models = (
        ('documents', 'documents'),
        ('notices', 'notice'),
        ('storage', 'item'),
        ('storage', 'places'),
        ('parking', 'vehicle'),
        ('amenities', 'booking'),
    )
    return _create_group('managers', models)


def create_residents_group():
    models = (
        ('notices', 'notice'),
        ('storage', 'item'),
        ('parking', 'vehicle'),
        ('amenities', 'booking'),
    )

    return _create_group('residents', models)
