import factory

from django.test import TestCase
from django.core import mail

from factory.django import DjangoModelFactory


from apps.buildings.tests import (
    SiteFactory,
    ApartmentFactory,
)


from .models import User
from .backends import ObjectPermissionBackend


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
    site = factory.SubFactory(SiteFactory)


class UserTests(TestCase):

    def test_email_sent_on_new_manager(self):

        ManagerFactory.create()
        self.assertEqual(len(mail.outbox), 1)

    def test_email_sent_on_new_resident(self):

        ResidentFactory.create()
        self.assertEqual(len(mail.outbox), 1)

    def test_delete(self):
        """Delete should deativate user & obfuscate email"""

        resident = ResidentFactory.create()
        resident.delete()

        self.assertEqual(User.objects.count(), 1)

        self.assertFalse(resident.is_active)
        self.assertNotEqual(resident.email, 'resident@gmail.com')
        self.assertEqual(resident.original_email, 'resident@gmail.com')

    def test_real_delete(self):

        resident = ResidentFactory.create()
        resident.real_delete()

        self.assertEqual(User.objects.count(), 0)


class ObjectPermissionBackendTests(TestCase):

    def test_model_permission(self):

        user = ManagerFactory.create()
        backend = ObjectPermissionBackend().has_perm(
            user, 'notices.add_notice'
        )

    def test_has_perms(self):

        user = ManagerFactory.create()

        self.assertTrue(user.has_perms(['notices.add_notice',
                                        'notices.change_notice']))

    def test_object_permission(self):

        class SomeModel(object):

            def has_permission(self, user, perm):
                if perm == 'somemodel_change':
                    return True
                return False

        user = User()

        obj = SomeModel()
        backend = ObjectPermissionBackend()

        self.assertTrue(backend.has_perm(user, 'somemodel_change', obj))
        self.assertFalse(backend.has_perm(user, 'somemodel_delete', obj))
