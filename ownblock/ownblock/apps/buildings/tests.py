
import factory

from django.db.models import signals
from django.test import TestCase
from django.contrib.sites.models import Site

from factory.django import DjangoModelFactory, mute_signals

from .models import Building, Apartment


class SiteFactory(DjangoModelFactory):

    class Meta:
        model = Site


@mute_signals(signals.pre_save)
class BuildingFactory(DjangoModelFactory):

    class Meta:
        model = Building

    address_1 = 'Pikisaarenkatu 48'
    city = 'Lappeenranta'
    postcode = '53900'
    country = 'FI'
    latitude = 60.1
    longitude = 20

    site = factory.SubFactory(SiteFactory)


class ApartmentFactory(DjangoModelFactory):

    class Meta:
        model = Apartment

    number = '1'
    floor = 1

    building = factory.SubFactory(BuildingFactory)


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
