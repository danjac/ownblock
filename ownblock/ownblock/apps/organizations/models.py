from django.db import models
from django.contrib.auth.models import Group

from model_utils import FieldTracker


class Organization(models.Model):

    name = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, null=True, blank=True)

    tracker = FieldTracker()

    def __str__(self):
        return self.name

    def save(self, **kwargs):

        if self.group is None or 'name' in self.tracker.changed():
            self.group = Group.objects.create(name="Org:%s" % self.name)

        super().save(**kwargs)
