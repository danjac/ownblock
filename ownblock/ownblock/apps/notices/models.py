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

    def can_edit_or_delete(self, user):
        if not user.is_authenticated():
            return False
        return user.role == 'resident' or user.id == self.author_id
