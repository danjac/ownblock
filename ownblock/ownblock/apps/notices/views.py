from django.conf import settings
from django.core.mail import send_mass_mail
from django.template import Context, loader
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from .models import Notice
from .serializers import NoticeSerializer


class NoticeViewSet(viewsets.ModelViewSet):

    model = Notice
    serializer_class = NoticeSerializer

    def pre_save(self, obj):
        obj.author = self.request.user
        obj.building = self.request.building

    def post_save(self, obj, created):

        if not created:
            return

        recipients = get_user_model().objects.filter(
            apartment__building=obj.building
        )

        site = self.request.site

        template = loader.get_template('notices/emails/new_notice.txt')
        messages = []
        subject = '%s: %s' % (site.name, obj.title)

        for recipient in recipients:
            message = template.render(Context({
                                              'notice': obj,
                                              'site': site,
                                              'recipient': recipient,
                                              }),
                                      )

            messages.append((subject,
                             message,
                             settings.DEFAULT_FROM_EMAIL,
                             [recipient.email]))

        send_mass_mail(tuple(messages))

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).select_related(
            'author',
            'author__apartment'
        ).order_by('-created')
