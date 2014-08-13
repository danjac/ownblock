from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManagerReadOnly

from .models import Amenity, Booking
from .permissions import IsBookingResidentOrManager
from .serializers import AmenitySerializer, BookingSerializer


class AmenityViewSet(viewsets.ModelViewSet):

    model = Amenity
    serializer_class = AmenitySerializer
    permission_classes = (IsResidentOrManagerReadOnly, )

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            building=self.request.building
        ).prefetch_related('booking_set').order_by('name')


class BookingViewSet(viewsets.ModelViewSet):

    model = Booking
    serializer_class = BookingSerializer
    permission_classes = (IsBookingResidentOrManager, )

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            amenity__building=self.request.building).select_related(
            'amenity',
            'resident',
        )
