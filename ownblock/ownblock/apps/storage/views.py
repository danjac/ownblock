from rest_framework import viewsets


from .models import Place, Item
from .serializers import PlaceSerializer, ItemSerializer


class PlaceViewSet(viewsets.ModelViewSet):

    model = Place
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('name')


class ItemViewSet(viewsets.ModelViewSet):

    model = Item
    serializer_class = ItemSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            place__building=self.request.building
        ).select_related(
            'place',
            'resident',
            'resident__apartment').order_by('description')
