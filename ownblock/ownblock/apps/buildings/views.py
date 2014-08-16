from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManagerReadOnly

from .models import Apartment
from .serializers import ApartmentSerializer


class ApartmentViewSet(viewsets.ReadOnlyModelViewSet):

    model = Apartment
    serializer_class = ApartmentSerializer
    permission_classes = (IsResidentOrManagerReadOnly, )

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).prefetch_related('user_set').order_by('number')
