from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManagerReadOnly

from .models import Place, Item
from .serializers import PlaceSerializer, ItemSerializer
from .permissions import IsOwnerOrManager


class PlaceViewSet(viewsets.ModelViewSet):

    model = Place
    serializer_class = PlaceSerializer
    permission_classes = (IsResidentOrManagerReadOnly, )

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('name')


class ItemViewSet(viewsets.ModelViewSet):

    model = Item
    serializer_class = ItemSerializer
    permission_classes = (IsOwnerOrManager,)

    def get_queryset(self):
        return super().get_queryset().filter(
            place__building=self.request.building
        ).select_related(
            'place',
            'resident',
            'place__building').order_by('description')
