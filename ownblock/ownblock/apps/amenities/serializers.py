from django.db.models.query import Q
from django.utils import timezone

from rest_framework import serializers

from .models import Amenity, Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id',
                  'resident',
                  'amenity',
                  'reserved_from',
                  'reserved_to')
        read_only_fields = ('resident',)

    def validate_amenity(self, attrs, source):
        value = attrs[source]
        if not value.is_available:
            raise serializers.ValidationError("Amenity not available")
        if not value in self.context['request'].building.amenity_set.all():
            raise serializers.ValidationError("Amenity not found")
        return attrs

    def validate_reserved_from(self, attrs, source):
        value = attrs[source]
        if value < timezone.now():
            raise serializers.ValidationError("Start date before present")
        return attrs

    def validate(self, attrs):
        if attrs['reserved_from'] > attrs['reserved_to']:
            raise serializers.ValdiationError("Start after end")
        bookings = attrs['amenity'].booking_set.all()
        date_range = (attrs['reserved_from'], attrs['reserved_to'])
        if bookings.filter(
            Q(reserved_from__range=date_range) |
                Q(reserved_to__range=date_range)).exists():
            raise serializers.ValidationError("Booking conflict")

        return attrs

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)


class AmenitySerializer(serializers.ModelSerializer):
    booking_set = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Amenity
        fields = ('id', 'name', 'is_available', 'booking_set')

    def save_object(self, obj, **kwargs):
        obj.building = self.context['request'].building
        return super().save_object(obj, **kwargs)
