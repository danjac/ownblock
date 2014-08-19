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

    def get_groups(self):
        return [self.resident,
                self.resident.apartment.building.organization.group]

    def has_permission(self, user, perm):
        if user.role == 'resident':
            return user == self.resident
        if user.role == 'manager':
            return (self.resident.apartment.building.organization_id ==
                    user.organization_id)
        return False
