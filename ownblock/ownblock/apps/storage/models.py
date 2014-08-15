from django.conf import settings
from django.db import models

from apps.buildings.models import Building


class Place(models.Model):

    name = models.CharField(max_length=60)
    building = models.ForeignKey(Building)

    def __str__(self):
        return self.name

    def can_edit_or_delete(self, user):
        if not user.is_authenticated() or user.role != 'manager':
            return False
        return user.organization_id == self.building.organization_id


class Item(models.Model):

    description = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=30, blank=True)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    place = models.ForeignKey(Place)

    def __str__(self):
        return self.description

    def can_edit_or_delete(self, user):
        if not user.is_authenticated():
            return False
        if user.id == self.resident.id:
            return True
        return self.place.can_edit_or_delete(user)
