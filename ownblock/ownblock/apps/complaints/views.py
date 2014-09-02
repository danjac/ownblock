from rest_framework import viewsets

from .models import Complaint
from .serializers import ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):

    model = Complaint
    serializer_class = ComplaintSerializer

    def post_save(self, obj):
        pass  # TBD: send email to all block managers

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs).filter(
            building=self.request.building
        ).order_by('-created')
        if self.request.user.role == 'resident':
            return qs.filter(resident=self.request.user)
        return qs
