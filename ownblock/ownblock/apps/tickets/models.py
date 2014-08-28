from django.conf import settings
from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

from apps.buildings.models import Building, Apartment
from apps.amenities.models import Amenity


class Ticket(TimeStampedModel):

    STATUS = Choices('new', 'accepted', 'resolved')

    status = StatusField()
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL)
    handler = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='handled_tickets',
                                null=True, blank=True)
    description = models.TextField()

    building = models.ForeignKey(Building)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)
    amenity = models.ForeignKey(Amenity, null=True, blank=True)

    # ticket is updated
    comment = models.TextField(blank=True)

    # ticket is resolved
    action = models.TextField(blank=True)

    def has_permission(self, user, perm):
        if user.role == 'manager':
            return self.building.site == user.site
        return False
