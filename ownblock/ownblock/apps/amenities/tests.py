import factory

from unittest.mock import Mock

from django.test import TestCase

from rest_framework import serializers

from factory.django import DjangoModelFactory

from apps.buildings.tests import (
    BuildingFactory
)

from .models import Amenity
from .serializers import BookingSerializer


class AmenityFactory(DjangoModelFactory):

    class Meta:
        model = Amenity

    name = "Sauna"
    building = factory.SubFactory(BuildingFactory)
    is_available = True


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
