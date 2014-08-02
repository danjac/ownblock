from django.db import models


class Organization(models.Model):

    name = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
