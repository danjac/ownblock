from django.db.models import Q
from rest_framework import viewsets


from .models import Ticket
from .serializers import TicketSerializer, ManagerTicketSerializer


class TicketViewSet(viewsets.ModelViewSet):

    model = Ticket
    serializer_class = TicketSerializer

    def get_serializer_class(self, **kwargs):
        if self.request.user.role == 'manager':
            return ManagerTicketSerializer
        return TicketSerializer

    def pre_save(self, obj):
        obj.reporter = self.request.user
        obj.building = self.request.building
        if self.request.user.role == 'resident':
            obj.apartment = self.request.user.apartment
        elif self.request.user.role == 'manager':
            obj.handler = self.request.user

    def post_save(self, obj, created):
        pass  # TBD: notify managers on create, notify reporter on change

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related(
            'reporter',
            'apartment',
            'reporter__apartment',).filter(
            building=self.request.building
        ).order_by('-created')

        if self.request.user.role == 'resident':
            qs = qs.filter(
                Q(reporter=self.request.user) |
                Q(apartment=self.request.user.apartment)
            )
        return qs
