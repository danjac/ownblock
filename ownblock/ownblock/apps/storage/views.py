from django.http import Http404, HttpResponse

from rest_framework import viewsets, parsers
from rest_framework.decorators import detail_route
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
    parser_classes = (parsers.MultiPartParser,
                      parsers.JSONParser,)

    @detail_route(methods=('PATCH',))
    def remove_photo(self, request, pk, *args, **kwargs):
        try:
            obj = self.get_queryset().filter(photo__isnull=False).get(pk=pk)
        except self.model.DoesNotExist():
            raise Http404()

        obj.delete_photo()
        return Response()

    @detail_route()
    def photo(self, request, pk, *args, **kwargs):
        try:
            obj = self.get_queryset().filter(photo__isnull=False).get(pk=pk)
        except self.model.DoesNotExist():
            raise Http404()

        response = HttpResponse(
            obj.photo, content_type=obj.get_photo_content_type())
        return response

    @detail_route()
    def thumbnail(self, request, pk, *args, **kwargs):
        try:
            obj = self.get_queryset().filter(photo__isnull=False).get(pk=pk)
        except self.model.DoesNotExist():
            raise Http404()

        tn = obj.get_thumbnail()
        if tn is None:
            raise Http404()

        response = HttpResponse(
            tn.read(), content_type=obj.get_photo_content_type())
        return response

    def pre_save(self, obj):
        if obj.resident_id is None:
            obj.resident = self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(
            place__building=self.request.building
        ).select_related(
            'place',
            'resident',
            'resident__apartment').order_by('description')
