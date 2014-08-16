from django.conf import settings
from django.db import models

from django_countries.fields import CountryField


class Vehicle(models.Model):

    description = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=12)
    country = CountryField(default="FI")
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_place = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.registration_number

    def can_edit_or_delete(self, user):
        if not user.is_authenticated():
            return False
        if self.resident_id == user.id:
            return True
        if (user.role == 'manager' and
                user.organization_id ==
                self.resident.apartment.building.organization_id):
            return True
        return False
