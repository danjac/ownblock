from unittest.mock import Mock

from django.test import TestCase

from rest_framework import serializers

from apps.accounts.tests import ResidentFactory
from apps.buildings.tests import ApartmentFactory

from .serializers import MessageSerializer


class SerializerTests(TestCase):

    def test_validate_recipient_if_same_as_sender(self):
        apt = ApartmentFactory.create()
        req = Mock()
        req.user = ResidentFactory.create(apartment=apt)
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': req.user}
        self.assertRaises(serializers.ValidationError,
                          serializer.validate_recipient, attrs, 'recipient')

    def test_validate_recipient_if_does_not_exist(self):
        apt = ApartmentFactory.create()
        req = Mock()
        req.user = ResidentFactory.create(apartment=apt)
        recipient = ResidentFactory.create()
        serializer = MessageSerializer(context={'request': req})
        attrs = {'recipient': recipient}
        self.assertRaises(serializers.ValidationError,
                          serializer.validate_recipient, attrs, 'recipient')

    def test_validate_recipient_if_ok(self):
        pass
