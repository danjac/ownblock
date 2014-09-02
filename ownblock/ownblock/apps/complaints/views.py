from rest_framework import viewsets

from .models import Complaint
from .serializers import ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):

    model = Complaint
    serializer_class = ComplaintSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.building = self.request.building

    def post_save(self, obj, created):
        pass  # TBD: send email to all block managers

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs).filter(
            building=self.request.building
        ).select_related(
            'apartment',
            'resident',
            'resident__apartment').order_by('-created')
        if self.request.user.role == 'resident':
            return qs.filter(resident=self.request.user)
        return qs
