from rest_framework import viewsets
from rest_framework.response import Response


from .models import Place, Item
from .serializers import PlaceSerializer, ItemSerializer


class PlaceViewSet(viewsets.ModelViewSet):

    model = Place
    serializer_class = PlaceSerializer

    def pre_save(self, obj):
        obj.building = self.request.building

    def retrieve(self, *args, **kwargs):

        self.object = self.get_object()
        context = {'request': self.request}
        data = PlaceSerializer(self.object, context=context).data
        items = self.object.item_set.select_related(
            'place',
            'resident',
            'resident__apartment',
        )
        data['items'] = ItemSerializer(
            items,
            many=True,
            context=context,
        ).data
        return Response(data)

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('name')


class ItemViewSet(viewsets.ModelViewSet):

    model = Item
    serializer_class = ItemSerializer

    def pre_save(self, obj):
        if obj.resident is None:
            obj.resident = self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(
            place__building=self.request.building
        ).select_related(
            'place',
            'resident',
            'resident__apartment').order_by('description')
