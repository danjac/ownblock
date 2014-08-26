from django.conf import settings
from django.core.mail import send_mail
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

        for recipient in recipients:

            send_mail('%s: %s' % (site.name, obj.title),
                      template.render(Context({
                                              'notice': obj,
                                              'site': site,
                                              'recipient': recipient,
                                              }),
                                      ),
                      settings.DEFAULT_FROM_EMAIL,
                      [recipient.email])

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('-created')
