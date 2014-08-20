from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsManager

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

    def send_new_resident_email(self, resident):
        token = default_token_generator.make_token(resident)
        uid = urlsafe_base64_encode
        pass

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
        ).prefetch_related('user_set').order_by('number')
