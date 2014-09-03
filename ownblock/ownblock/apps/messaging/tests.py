from unittest.mock import Mock

from django.test import TestCase

from rest_framework import serializers

from ..accounts.tests import ResidentFactory
from ..buildings.tests import ApartmentFactory, BuildingFactory

from .serializers import MessageSerializer


class SerializerTests(TestCase):

    def test_validate_recipient_if_same_as_sender(self):
        apt = ApartmentFactory.create()
        req = Mock()
        req.building = apt.building
        req.user = ResidentFactory.create(apartment=apt,
                                          email="test@gmail.com")
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': req.user}
        self.assertRaises(serializers.ValidationError,
                          serializer.validate_recipient, attrs, 'recipient')

    def test_validate_recipient_if_not_resident(self):
        bdg = BuildingFactory.create(postcode='387383')
        apt = ApartmentFactory.create(building=bdg)
        req = Mock()
        req.building = apt.building
        req.user = ResidentFactory.create(apartment=apt)
        recipient = ResidentFactory.create(email="test2@gmail.com")
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': recipient}
        self.assertRaises(serializers.ValidationError,
                          serializer.validate_recipient, attrs, 'recipient')

    def test_validate_recipient_if_not_manager(self):
        bdg = BuildingFactory.create(postcode='387383')
        apt = ApartmentFactory.create(building=bdg)
        req = Mock()
        req.building = apt.building
        req.user = ResidentFactory.create(apartment=apt)
        recipient = ResidentFactory.create(email="test2@gmail.com")
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': recipient}
        self.assertRaises(serializers.ValidationError,
                          serializer.validate_recipient, attrs, 'recipient')

    def test_validate_recipient_if_all_ok(self):
        apt = ApartmentFactory.create()
        req = Mock()
        req.building = apt.building
        req.user = ResidentFactory.create(apartment=apt)
        recipient = ResidentFactory.create(apartment=apt,
                                           email='other@gmail.com')
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': recipient}
        serializer.validate_recipient(attrs, 'recipient')
