from django.db import models

from geopy.geocoders import Nominatim

from model_utils import FieldTracker

from django_countries.fields import CountryField

from apps.organizations.models import Organization

_geolocator = Nominatim()


class Building(models.Model):

    organization = models.ForeignKey(Organization)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=12)
    country = CountryField(default='FI')

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    tracker = FieldTracker(fields=('address_1',
                                   'address_2',
                                   'city',
                                   'postcode',
                                   'country'))

    def __str__(self):
        return self.get_full_address()

    def get_full_address(self):
        return ", ".join((self.address_1 + self.address_2,
                          self.city,
                          self.postcode,
                          str(self.country.name)))

    def save(self, *args, **kwargs):
        has_changed = any([self.tracker.has_changed(field) for
                           field in self.tracker.fields])
        if has_changed or None in (self.latitude, self.longitude):
            location = _geolocator.geocode(self.get_full_address())
            self.latitude, self.longitude = (location.latitude,
                                             location.longitude)
        return super().save(*args, **kwargs)


class Apartment(models.Model):

    building = models.ForeignKey(Building)
    number = models.CharField(max_length=3)
    floor = models.PositiveIntegerField()

    owner_name = models.CharField(max_length=60, blank=True)
    owner_phone = models.CharField(max_length=12, blank=True)
    owner_email = models.EmailField(blank=True)

    def __str__(self):
        return "#%s" % self.number
