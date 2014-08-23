from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsManager
from apps.storage.models import Item
from apps.parking.models import Vehicle

from .models import Apartment, Building

from .serializers import (
    ApartmentSerializer,
    BuildingSerializer,
    ResidentSerializer,
)


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):

    model = Building
    serializer_class = BuildingSerializer
    permission_classes = (permissions.IsAuthenticated, IsManager,)

    def get_queryset(self):
        return super().get_queryset().filter(
            site=self.request.user.site_id
        ).order_by('city', 'address_1', 'postcode')

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.session['building_id'] = self.object.id
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class ApartmentViewSet(viewsets.ReadOnlyModelViewSet):

    model = Apartment
    serializer_class = ApartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_serializer(self.object).data

        users = self.object.user_set.filter(is_active=True)

        data['users'] = ResidentSerializer(
            self.object,
            users,
            many=True).data

        items = Item.objects.filter(
            resident__apartment=self.object
        ).select_related('place')

        data['items'] = []

        for item in items.iterator():
            data['items'].append({
                'id': item.id,
                'description': item.description,
                'place': {
                    'id': item.place.id,
                    'name': item.place.name,
                }
            })

        vehicles = Vehicle.objects.filter(
            resident__apartment=self.object
        )

        data['vehicles'] = []

        for vehicle in vehicles.iterator():
            data['vehicles'].append({
                'id': vehicle.id,
                'description': vehicle.description,
                'registration_number': vehicle.registration_number,
            })

        return Response(data)

    @action(permission_classes=(IsManager,))
    def add_resident(self, request, pk=None):
        obj = self.get_object()
        serializer = ResidentSerializer(data=request.DATA, apartment=obj)

        if serializer.is_valid():

            user = serializer.object
            user.apartment = obj
            user.set_unusable_password()
            user.role = 'resident'

            serializer.save(force_insert=True)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).prefetch_related('user_set').order_by('floor', 'number')
