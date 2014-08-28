from rest_framework import viewsets

from apps.accounts.permissions import IsResident, IsManager

from .models import Ticket
from .serializers import TicketSerializer, ManagerTicketSerializer


class ResidentTicketViewSet(viewsets.ModelViewSet):

    model = Ticket

    serializer_class = TicketSerializer

    permission_classes = (
        IsResident,
    )

    def pre_save(self, obj):
        obj.reporter = self.request.user
        obj.apartment = self.request.user.apartment
        obj.building = self.request.building

    def post_save(self, obj, created):
        pass  # TBD: notify managers on create, notify reporter on change

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(
            apartment=self.request.user.apartment
        ).order_by('-created')


class ManagerTicketViewSet(viewsets.ModelViewSet):

    model = Ticket

    serializer_class = ManagerTicketSerializer

    permission_classes = (
        IsManager,
    )

    def pre_save(self, obj):
        obj.reporter = self.request.user
        obj.building = self.request.building

    def post_save(self, obj, created):
        pass  # notify apartment residents, other managers

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(building=self.rquest.building).order_by('-created')
