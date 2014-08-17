import factory

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import Group

from factory.django import DjangoModelFactory

from guardian.shortcuts import get_perms

from model_utils import FieldTracker

from apps.buildings.tests import (
    OrganizationFactory,
    BuildingFactory,
    ApartmentFactory,
)

from apps.buildings.models import Building

from .models import User, DefaultPermissionsMixin


class ResidentFactory(DjangoModelFactory):

    class Meta:
        model = User

    role = 'resident'
    apartment = factory.SubFactory(ApartmentFactory)
    email = 'resident@gmail.com'


class ManagerFactory(DjangoModelFactory):

    class Meta:
        model = User

    role = 'manager'
    email = 'manager@gmail.com'
    organization = factory.SubFactory(OrganizationFactory)


class UserTests(TestCase):

    def test_assign_groups_to_resident(self):

        user = ResidentFactory.create()
        group = user.groups.all()[0]
        self.assertEqual(group.name, 'residents')
        self.assertTrue(user.has_perm('notices.add_notice'))

    def test_assign_groups_to_manager(self):

        user = ManagerFactory.create()
        groups = [g.name for g in user.groups.all()]

        self.assertTrue('managers' in groups)
        self.assertTrue('Org:%s' % user.organization.name in groups)

        self.assertTrue(user.has_perm('notices.add_notice'))


class DefaultPermissionsMixinTests(TestCase):

    class SampleModel(DefaultPermissionsMixin, models.Model):

        name = models.CharField(max_length=10)
        user = models.ForeignKey(User)
        group = models.ForeignKey(Group)

        permission_tracker = FieldTracker(fields=('user', 'group'))

        class Meta:
            app_label = 'accounts'

        def get_groups(self):
            return [self.user, self.group]

    def test_assign_new_permissions(self):

        user = ResidentFactory()
        group = user.apartment.building.organization.group

        obj = self.SampleModel.objects.create(user=user, group=group)

        self.assertTrue(user.has_perm('accounts.add_samplemodel', obj))
        self.assertTrue(user.has_perm('accounts.change_samplemodel', obj))
        self.assertTrue(user.has_perm('accounts.delete_samplemodel', obj))

        self.assertTrue('add_samplemodel' in get_perms(group, obj))
        self.assertTrue('change_samplemodel' in get_perms(group, obj))
        self.assertTrue('delete_samplemodel' in get_perms(group, obj))

    def test_change_permissions(self):

        user = ResidentFactory()
        group = user.apartment.building.organization.group

        obj = self.SampleModel.objects.create(user=user, group=group)

        self.assertTrue(user.has_perm('accounts.change_samplemodel', obj))

        user2 = ResidentFactory.create(
            email='user2@gmail.com',
            apartment=user.apartment
        )

        obj.user = user2
        obj.save()

        user = User.objects.get(pk=user.id)

        self.assertFalse(user.has_perm('accounts.change_samplemodel', obj))
        self.assertTrue(user2.has_perm('accounts.change_samplemodel', obj))

        self.assertTrue('add_samplemodel' in get_perms(group, obj))
        self.assertTrue('change_samplemodel' in get_perms(group, obj))
        self.assertTrue('delete_samplemodel' in get_perms(group, obj))
