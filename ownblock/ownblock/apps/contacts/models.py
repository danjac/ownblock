from django.db import models

from apps.buildings.models import Building


class Contact(models.Model):

    building = models.ForeignKey(Building)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
