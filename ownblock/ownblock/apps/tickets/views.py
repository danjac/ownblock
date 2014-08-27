from django.db.models import Q
from rest_framework import viewsets

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):

    model = Ticket
    serializer_class = TicketSerializer

    def pre_save(self, obj):
        if obj.reporter_id is None:
            obj.reporter = self.request.user

    def post_save(self, obj, created):
        pass  # TBD: notify managers on create, notify reporter on change

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            building=self.request.building
        ).order_by('-created').select_related(
            'apartment',
            'reporter',
            'amenity')

        if self.request.user.role == 'manager':
            return qs

        return qs.filter(Q(apartment=self.request.user.apartment) |
                         Q(reporter=self.request.user))
