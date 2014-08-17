from django.conf import settings
from django.db import models

from guardian.shortcuts import assign_perm

from django_countries.fields import CountryField


class Vehicle(models.Model):

    description = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=12)
    country = CountryField(default="FI")
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_place = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.registration_number

    def save(self, **kwargs):
        super().save(**kwargs)

        perms = ('parking.change_vehicle', 'parking.delete_vehicle')

        org_group = self.resident.apartment.building.organization.group

        for perm in perms:
            assign_perm(perm, self.resident, self)
            assign_perm(perm, org_group, self)
