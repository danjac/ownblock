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
        # TBD: validate booking conflicts
        return attrs

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)


class AmenitySerializer(serializers.ModelSerializer):
    booking_set = BookingSerializer(many=True)

    class Meta:
        model = Amenity
        fields = ('id', 'name', 'is_available', 'booking_set')
