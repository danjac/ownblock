from django.db import models
from django.contrib.auth.models import Group


class Organization(models.Model):

    name = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if self.group is None:
            self.group = Group.objects.create(name="Org %s" % self.name)

        return super().save(**kwargs)
