from django.db import models

from django_countries.fields import CountryField

from apps.organizations.models import Organization


class Building(models.Model):

    organization = models.ForeignKey(Organization)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=12)
    country = CountryField(default='FI')

    def __str__(self):
        return self.get_full_address()

    def get_full_address(self):
        return ", ".join((self.address1 + self.address2,
                          self.city,
                          self.postcode,
                          self.country.name))


class Apartment(models.Model):

    building = models.ForeignKey(Building)
    number = models.CharField(max_length=3)
    floor = models.PositiveIntegerField()

    owner_name = models.CharField(max_length=60, blank=True)
    owner_phone = models.CharField(max_length=12, blank=True)
    owner_email = models.EmailField(blank=True)

    def __str__(self):
        return "#%s" % self.number
