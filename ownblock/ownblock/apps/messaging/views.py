from django.conf import settings
from django.db.models.query import Q
from django.core.mail import send_mail
from django.template import Context, loader

from rest_framework import viewsets

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):

    model = Message
    serializer_class = MessageSerializer

    def post_save(self, obj, created):

        if not created:
            return

        template = loader.get_template("messaging/emails/new_message.txt")

        send_mail(
            '{}: You have received a new message'.format(
                self.request.site.name
            ),
            template.render(
                Context(
                    {
                        'message': obj,
                        'site': self.request.site,
                    })),
            settings.DEFAULT_FROM_EMAIL,
            [obj.recipient.email],
        )

    def pre_save(self, obj):
        obj.sender = self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(recipient=self.request.user) |
            Q(sender=self.request.user)
        ).select_related('sender', 'recipient').order_by('-created')
