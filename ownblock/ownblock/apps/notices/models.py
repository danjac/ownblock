from django.conf import settings
from django.db import models

from guardian.shortcuts import assign_perm

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
        """DEPRECATED"""
        if not user.is_authenticated():
            return False
        if user.id == self.author.id:
            return True
        if user.role == 'manager':
            return self.building.organization_id == user.organization_id
        return False

    def save(self, **kwargs):
        super().save(**kwargs)
        for group in (self.author, self.building.organization.group):
            assign_perm('notices.change_notice', group, self)
            assign_perm('notices.delete_notice', group, self)
