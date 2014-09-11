from django.db import models
from django.core.validators import RegexValidator


from model_utils.models import TimeStampedModel

RE_DOMAIN = r'[0-9a-zA-Z]+'


class Signup(TimeStampedModel):

    name = models.CharField(max_length=60, unique=True)
    contact_name = models.CharField(max_length=80)
    email = models.EmailField()
    domain = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(RE_DOMAIN,
                                   'Not a valid domain')])
    phone = models.CharField(max_length=20, blank=True)
    num_buildings = models.PositiveIntegerField()
    num_apartments = models.PositiveIntegerField()
    questions = models.TextField(blank=True)

    def __str__(self):
        return self.name
