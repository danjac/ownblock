import factory

from django.test import TestCase
from django.db import models

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
