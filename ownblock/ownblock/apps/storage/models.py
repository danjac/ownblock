from django.conf import settings
from django.db import models

from model_utils import FieldTracker

from apps.accounts.models import DefaultPermissionsMixin

from apps.buildings.models import Building


class Place(DefaultPermissionsMixin, models.Model):

    name = models.CharField(max_length=60)
    building = models.ForeignKey(Building)

    permission_tracker = FieldTracker(fields=('building',))

    def __str__(self):
        return self.name

    def get_groups(self):
        return [self.building.organization.group]


class Item(DefaultPermissionsMixin, models.Model):

    description = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=30, blank=True)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    place = models.ForeignKey(Place)

    permission_tracker = FieldTracker(fields=('resident', 'place'))

    def __str__(self):
        return self.description

    def get_groups(self):
        return [self.place.building.organization.group,
                self.resident]
