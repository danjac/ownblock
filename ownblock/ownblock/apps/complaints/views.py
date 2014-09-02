from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, loader

from rest_framework import viewsets

from .models import Complaint
from .serializers import ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):

    model = Complaint
    serializer_class = ComplaintSerializer

    def pre_save(self, obj):
        obj.resident = self.request.user
        obj.building = self.request.building

    def post_save(self, obj, created):
        if not created:
            return
        template = loader.get_template('complaints/emails/new_complaint.txt')
        for manager in obj.building.site.user_set.all():
            message = template.render(Context({
                'complaint': obj,
                'manager': manager,
                'site': obj.building.site,
            }))
            send_mail('A new complaint has been sent',
                      message,
                      settings.DEFAULT_FROM_EMAIL,
                      [manager.email])

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs).filter(
            building=self.request.building
        ).select_related(
            'apartment',
            'resident',
            'resident__apartment').order_by('-created')
        if self.request.user.role == 'resident':
            qs = qs.filter(resident=self.request.user)
        return qs
