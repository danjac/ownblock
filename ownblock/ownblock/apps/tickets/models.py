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
    description = models.TextField()

    building = models.ForeignKey(Building)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)
    amenity = models.ForeignKey(Amenity, null=True, blank=True)

    def has_permission(self, user, perm):
        if user.role == 'manager':
            return True
        return False


class Comment(TimeStampedModel):

    ticket = models.ForeignKey(Ticket)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField()

    def has_permission(self, user, perm):
        return self.author == user or self.user.role == 'manager'
