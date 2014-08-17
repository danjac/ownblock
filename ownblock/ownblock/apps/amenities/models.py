from django.conf import settings
from django.db import models

from model_utils import FieldTracker


from apps.accounts.models import DefaultPermissionsMixin

from apps.buildings.models import Building


class Amenity(DefaultPermissionsMixin, models.Model):

    name = models.CharField(max_length=60)
    building = models.ForeignKey(Building)
    is_available = models.BooleanField(default=True)

    permission_tracker = FieldTracker(fields=('building', ))

    def get_groups(self):
        return [self.building.organization.group]

    class Meta:
        verbose_name_plural = 'amenities'

    def __str__(self):
        return self.name


class Booking(DefaultPermissionsMixin, models.Model):

    amenity = models.ForeignKey(Amenity)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()

    permission_tracker = FieldTracker(fields=('building', 'amenity'))

    def get_groups(self):
        return [self.amenity.building.organization.group,
                self.resident]
