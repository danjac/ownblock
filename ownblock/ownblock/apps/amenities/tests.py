import factory

from unittest.mock import Mock

from django.test import TestCase

from rest_framework import serializers

from factory.django import DjangoModelFactory

from apps.accounts.tests import ResidentFactory
from apps.buildings.tests import BuildingFactory

from .models import Amenity, Booking
from .serializers import BookingSerializer


class AmenityFactory(DjangoModelFactory):

    class Meta:
        model = Amenity

    name = "Sauna"
    building = factory.SubFactory(BuildingFactory)
    is_available = True


class BookingFactory(DjangoModelFactory):

    class Meta:
        model = Booking

    resident = factory.SubFactory(ResidentFactory)
    amenity = factory.SubFactory(AmenityFactory)


class BookingSerializerTests(TestCase):

    def test_validate_amenity_if_available(self):

        amenity = AmenityFactory(is_available=True)
        request = Mock()
        request.building = amenity.building

        attrs = {'amenity': amenity}
        source = 'amenity'
        serializer = BookingSerializer(context={'request': request})
        serializer.validate_amenity(attrs, source)

    def test_validate_amenity_if_not_available(self):

        amenity = AmenityFactory(is_available=False)
        request = Mock()
        request.building = amenity.building

        attrs = {'amenity': amenity}
        source = 'amenity'
        serializer = BookingSerializer(context={'request': request})
        self.assertRaises(
            serializers.ValidationError,
            serializer.validate_amenity, attrs, source)

    def test_validate_amenity_if_does_not_exist(self):

        amenity = AmenityFactory.create()

        request = Mock()
        # different building
        request.building = BuildingFactory.create(address_1='Sesame St')

        attrs = {'amenity': amenity}
        source = 'amenity'
        serializer = BookingSerializer(context={'request': request})
        self.assertRaises(
            serializers.ValidationError,
            serializer.validate_amenity, attrs, source)

    def test_validate_amenity_if_conflicting_dates(self):

        booking = BookingFactory.create(reserved_from=date_from,
                                        reserved_to=date_to)
