from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManagerReadOnly

from .models import Amenity
from .serializers import AmenitySerializer


class AmenityViewSet(viewsets.ModelViewSet):

    model = Amenity
    serializer_class = AmenitySerializer
    permission_classes = (IsResidentOrManagerReadOnly, )

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            building=self.request.building
        ).order_by('name')
