from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from rest_framework import viewsets


from .models import Ticket
from .serializers import TicketSerializer, ManagerTicketSerializer


User = get_user_model()


class TicketViewSet(viewsets.ModelViewSet):

    model = Ticket
    serializer_class = TicketSerializer

    def get_serializer_class(self, **kwargs):
        if self.request.user.role == 'manager':
            return ManagerTicketSerializer
        return TicketSerializer

    def pre_save(self, obj):
        if obj.reporter_id is None:
            obj.reporter = self.request.user
        obj.building = self.request.building
        if self.request.user.role == 'resident' and not obj.amenity_id:
            obj.apartment = self.request.user.apartment
        elif self.request.user.role == 'manager':
            obj.handler = self.request.user

    def post_save(self, obj, created):

        recipients = User.objects.filter(
            role='manager',
            site=obj.building.site
        )

        if obj.apartment:
            recipients = recipients | User.objects.filter(
                role='resident',
                apartment=obj.apartment,
            )

        recipients = recipients.exclude(pk=self.request.user.id)

        template = loader.get_template('tickets/emails/notification.txt')

        for recipient in recipients:
            ctx = Context({
                'ticket': obj,
                'created': created,
                'recipient': recipient,
                'site': obj.building.site,
            })

            message = template.render(ctx)
            subject = '%s: new issue' if created else '%s: issue updated'
            subject = subject % obj.building.site.name

            send_mail(subject,
                      message,
                      settings.DEFAULT_FROM_EMAIL,
                      [recipient.email])

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related(
            'reporter',
            'apartment',
            'handler',
            'amenity',
            'reporter__apartment',).filter(
            building=self.request.building
        ).order_by('-created')

        if self.request.user.role == 'resident':
            qs = qs.filter(
                Q(reporter=self.request.user) |
                Q(apartment=self.request.user.apartment)
            )
        return qs
