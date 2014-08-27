from rest_framework import viewsets

from apps.accounts.permissions import IsResident

from .models import Ticket
from .serializers import ResidentTicketSerializer


class ResidentTicketViewSet(viewsets.ModelViewSet):

    model = Ticket

    serializer_class = ResidentTicketSerializer

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
