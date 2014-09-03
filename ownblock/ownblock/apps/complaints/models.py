from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel

from ..buildings.models import Apartment, Building


class Complaint(TimeStampedModel):

    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    building = models.ForeignKey(Building)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)
    complaint = models.TextField()
