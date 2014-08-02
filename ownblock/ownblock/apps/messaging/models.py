from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel


class Message(TimeStampedModel):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='received_messages')
    parent = models.ForeignKey('self', null=True, blank=True)
    header = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.header
