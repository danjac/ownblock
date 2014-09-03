from django.db import models

from ..buildings.models import Building


class Contact(models.Model):

    building = models.ForeignKey(Building)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    available_hours = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def has_permission(self, user, perm):
        return self.building.site_id == user.site_id
