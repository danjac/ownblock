from rest_framework import viewsets, permissions
from rest_framework.response import Response

from apps.accounts.permissions import IsManager

from .models import Apartment, Building
from .serializers import ApartmentSerializer, BuildingSerializer


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):

    model = Building
    serializer_class = BuildingSerializer
    permission_classes = (permissions.IsAuthenticated, IsManager,)

    def get_queryset(self):
        return super().get_queryset().filter(
            organization=self.request.user.organization
        ).order_by('city', 'address_1', 'postcode')

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.session['building_id'] = self.object.id
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class ApartmentViewSet(viewsets.ReadOnlyModelViewSet):

    model = Apartment
    serializer_class = ApartmentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).prefetch_related('user_set').order_by('number')
