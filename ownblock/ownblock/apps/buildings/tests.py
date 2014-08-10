
import factory

from django.test import TestCase

from factory.django import DjangoModelFactory

from apps.organizations.models import Organization

from .models import Building


class OrganizationFactory(DjangoModelFactory):

    class Meta:
        model = Organization

    name = 'Org 1'


class BuildingFactory(DjangoModelFactory):

    class Meta:
        model = Building

    address_1 = 'Pikisaarenkatu 48'
    city = 'Lappeenranta'
    postcode = '53900'
    country = 'FI'

    organization = factory.SubFactory(OrganizationFactory)


class BuildingTests(TestCase):

    def test_set_lat_lng_if_none(self):
        bdg = BuildingFactory()
        bdg.save()
        self.assertNotEqual(bdg.latitude, None)
        self.assertNotEqual(bdg.longitude, None)

    def test_set_lat_lng_if_changed(self):
        bdg = BuildingFactory()
        bdg.save()
        lat, lng = bdg.latitude, bdg.longitude

        bdg.address_1 = 'Raastuvankatu 28'
        bdg.save()

        self.assertNotEqual(bdg.latitude, lat)
        self.assertNotEqual(bdg.longitude, lng)
