from django.conf import settings
from django.db import models

from model_utils import FieldTracker

from apps.accounts.models import DefaultPermissionsMixin

from django_countries.fields import CountryField


class Vehicle(DefaultPermissionsMixin, models.Model):

    description = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=12)
    country = CountryField(default="FI")
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_place = models.CharField(max_length=12, blank=True)

    permission_tracker = FieldTracker(fields=('resident',))

    def __str__(self):
        return self.registration_number

    def get_groups(self):
        return [self.resident,
                self.resident.apartment.building.organization.group]
