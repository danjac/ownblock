from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel

from apps.buildings.models import Building


class Notice(TimeStampedModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    building = models.ForeignKey(Building)
    title = models.CharField(max_length=100)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def has_permission(self, user, perm):

        if (user.role == 'manager' and
                user.site_id == self.building.site_id):
            return True

        if (user.role == 'resident' and user == self.author):
            return True

        return False
