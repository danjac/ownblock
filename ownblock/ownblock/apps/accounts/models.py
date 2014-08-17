from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)

from rest_framework.compat import get_model_name

from guardian.shortcuts import (
    assign_perm,
    remove_perm,
    get_users_with_perms,
    get_groups_with_perms,
)


from model_utils import Choices, FieldTracker


from apps.organizations.models import Organization
from apps.buildings.models import Apartment


class DefaultPermissionsMixin(object):

    """
    Automatically assigns default permissions to an object
    on save.
    """

    def get_groups(self):
        raise NotImplemented()

    def save(self, **kwargs):
        if not hasattr(self, 'permission_tracker'):
            raise AttributeError('You must implement permission_tracker')

        has_changed = bool(self.permission_tracker.changed())

        super().save(**kwargs)

        if not has_changed:
            return

        groups_for_addition = self.get_groups()

        # check existing perms for removal

        groups_for_deletion = [u for u in get_users_with_perms(self) if
                               u not in groups_for_addition]

        groups_for_deletion += [g for g in get_groups_with_perms(self) if
                                g not in groups_for_addition]

        permissions = getattr(self._meta, 'permissions', None)

        if not permissions:
            model_name = get_model_name(self)
            app_label = self._meta.app_label
            permissions = [
                "%s.add_%s" % (app_label, model_name),
                "%s.change_%s" % (app_label, model_name),
                "%s.delete_%s" % (app_label, model_name),
            ]
        for group in groups_for_addition:
            for perm in permissions:
                assign_perm(perm, group, self)
        for group in groups_for_deletion:
            for perm in permissions:
                remove_perm(perm, group, self)


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
    """Create top-level group"""
    group, created = Group.objects.get_or_create(name=name)
    if not created:
        return group

    # this is OK for now, may require more complex lookups later
    permissions = ('add', 'change', 'delete')

    for app_label, model in models:
        for perm in permissions:
            assign_perm('%s.%s_%s' % (app_label, perm, model), group)

    return group


def create_managers_group():
    models = (
        ('amenities', 'amenity'),
        ('amenities', 'booking'),
        ('contacts', 'contact'),
        ('documents', 'document'),
        ('messaging', 'message'),
        ('notices', 'notice'),
        ('parking', 'vehicle'),
        ('storage', 'item'),
        ('storage', 'place'),
    )
    return _create_group('managers', models)


def create_residents_group():
    models = (
        ('amenities', 'booking'),
        ('notices', 'notice'),
        ('messaging', 'message'),
        ('parking', 'vehicle'),
        ('storage', 'item'),
    )

    return _create_group('residents', models)
