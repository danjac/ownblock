from django.conf import settings
from django.db import models
from django.db.models import signals
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.sites.models import Site

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


def send_message_email(sender, instance, created, **kwargs):
    if not created:
        return

    template = loader.get_template("messaging/emails/new_message.txt")
    site = Site.objects.get_current()

    send_mail(
        '%s: You have received a new message' % site.name,
        template.render(
            Context(
                {
                    'message': instance,
                    'site': site,
                })),
        settings.DEFAULT_FROM_EMAIL,
        [instance.recipient.email],
    )


signals.post_save.connect(send_message_email,
                          sender=Message,
                          dispatch_uid="messaging.send_message_email")
