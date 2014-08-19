from django.conf import settings
from django.db import models

from apps.buildings.models import Building


class Amenity(models.Model):

    name = models.CharField(max_length=60)
    building = models.ForeignKey(Building)
    is_available = models.BooleanField(default=True)

    def get_groups(self):
        return [self.building.organization.group]

    class Meta:
        verbose_name_plural = 'amenities'

    def __str__(self):
        return self.name

    def has_permission(self, user, perm):
        return (user.role == 'manager' and
                user.organization_id == self.building.organization_id)


class Booking(models.Model):

    amenity = models.ForeignKey(Amenity)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()

    def has_permission(self, user, perm):
        if user.role == 'resident':
            return user == self.resident
        if user.role == 'manager':
            return (self.amenity.building.organization_id ==
                    user.organization_id)
        return False
