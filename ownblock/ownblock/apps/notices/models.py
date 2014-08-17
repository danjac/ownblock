from django.conf import settings
from django.db import models
from django.db.models import signals
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

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


def send_notice_email(sender, instance, created, **kwargs):

    if not created:
        return

    recipients = get_user_model().objects.filter(
        apartment__building=instance.building
    )

    site = Site.objects.get_current()

    template = loader.get_template('notices/emails/new_notice.txt')

    for recipient in recipients:

        send_mail('%s: %s' % (site.name, instance.title),
                  template.render(Context({
                                          'notice': instance,
                                          'site': site,
                                          'recipient': recipient,
                                          }),
                                  ),
                  settings.DEFAULT_FROM_EMAIL,
                  [recipient.email])

signals.post_save.connect(send_notice_email,
                          sender=Notice,
                          dispatch_uid='notices.send_notice_email')
