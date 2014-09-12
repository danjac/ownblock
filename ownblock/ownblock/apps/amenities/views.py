from rest_framework import viewsets
from rest_framework.response import Response

from .models import Amenity, Booking
from .serializers import AmenitySerializer, BookingSerializer


class AmenityViewSet(viewsets.ModelViewSet):

    model = Amenity
    serializer_class = AmenitySerializer

    def pre_save(self, obj):
        obj.building = self.request.building

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()

        data = self.get_serializer(self.object).data
        data['bookings'] = []
        for booking in self.object.booking_set.all():
            data['bookings'].append({
                'id': booking.id,
                'reserved_from': booking.reserved_from,
                'reserved_to': booking.reserved_to,
                'resident': booking.resident_id,
            })

        data['tickets'] = []
        for ticket in self.object.ticket_set.order_by('-created'):
            data['tickets'].append({
                'id': ticket.id,
                'created': ticket.created,
                'status': ticket.status,
                'description': ticket.description,
            })

        return Response(data)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            building=self.request.building
        ).prefetch_related('booking_set').order_by('name')


class BookingViewSet(viewsets.ModelViewSet):

    model = Booking
    serializer_class = BookingSerializer

    def pre_save(self, obj):
        obj.resident = self.request.user

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            amenity__building=self.request.building).select_related(
            'amenity',
            'resident',
            'resident__apartment',
            'resident__apartment__building',
        )
