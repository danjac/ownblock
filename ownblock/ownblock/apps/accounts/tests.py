import factory

from django.test import TestCase
from django.core import mail

from factory.django import DjangoModelFactory


from apps.buildings.tests import (
    OrganizationFactory,
    BuildingFactory,
    ApartmentFactory,
)

from apps.buildings.models import Building

from .models import User


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
