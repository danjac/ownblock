import factory

from django.test import TestCase

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


class SignalsTests(TestCase):

    def test_assign_groups_to_manager(self):

        building = BuildingFactory.create()

        manager = ManagerFactory.create(organization=building.organization)
        groups = [g.name for g in manager.groups.all()]
        self.assertTrue(
            'building-%s-managers' % building.id in groups
        )
        self.assertTrue('managers' in groups)

    def test_assign_groups_to_resident(self):

        resident = ResidentFactory.create()
        building = Building.objects.get()
        groups = [g.name for g in resident.groups.all()]
        self.assertTrue(
            'building-%s-residents' % building.id in groups
        )
        self.assertTrue('residents' in groups)
