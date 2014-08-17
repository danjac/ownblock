from rest_framework import viewsets

from .models import Amenity, Booking
from .serializers import AmenitySerializer, BookingSerializer


class AmenityViewSet(viewsets.ModelViewSet):

    model = Amenity
    serializer_class = AmenitySerializer

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            building=self.request.building
        ).prefetch_related('booking_set').order_by('name')


class BookingViewSet(viewsets.ModelViewSet):

    model = Booking
    serializer_class = BookingSerializer

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            amenity__building=self.request.building).select_related(
            'amenity',
            'resident',
        )
