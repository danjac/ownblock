from django.conf import settings
from django.db import models

from model_utils import FieldTracker
from model_utils.models import TimeStampedModel

from apps.accounts.models import DefaultPermissionsMixin
from apps.buildings.models import Building


class Notice(DefaultPermissionsMixin, TimeStampedModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    building = models.ForeignKey(Building)
    title = models.CharField(max_length=100)
    details = models.TextField(blank=True)

    permission_tracker = FieldTracker(fields=('building', 'author'))

    def __str__(self):
        return self.title

    def get_groups(self):
        return [self.author, self.building.organization.group]
