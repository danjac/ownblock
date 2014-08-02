from django.conf import settings
from django.db import models


from apps.buildings.models import Building


class Amenity(models.Model):

    name = models.CharField(max_length=60)
    building = models.ForeignKey(Building)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'amenities'

    def __str__(self):
        return self.name
