import datetime

from rest_framework import serializers

from apps.accounts.serializers import UserRelatedField

from .models import Amenity, Booking


class BookingRelatedField(serializers.RelatedField):

    class Meta:
        model = Booking
        fields = ('id',
                  'resident',
                  'amenity',
                  'reserved_from',
                  'reserved_to')


class AmenitySerializer(serializers.ModelSerializer):
    bookings = BookingRelatedField(many=True, source='booking_set')

    class Meta:
        model = Amenity
        fields = ('id', 'name', 'is_available', 'booking_set')


class BookingSerializer(serializers.ModelSerializer):
    resident = UserRelatedField(source='resident', read_only=True)

    class Meta:
        model = Booking
        fields = ('id',
                  'resident',
                  'amenity',
                  'reserved_from',
                  'reserved_to')

        read_only_fields = ('amenity', )

    def validate_amenity(self, attrs, source):
        value = attrs[source]
        if not self.context['request'].building.amenity_set.filter(
                pk=value, is_available=True).exists():
            raise serializers.ValidationError("Amenity not found")
        return attrs

    def validate_reserved_from(self, attrs, source):
        value = attrs[source]
        if value < datetime.datetime.now():
            raise serializers.ValidationError("Start date before present")
        return attrs

    def validate(self, attrs):
        if attrs['reserved_from'] > attrs['reserved_to']:
            raise serializers.ValdiationError("Start after end")
        # TBD: validate booking conflicts
        return attrs

    def save_object(self, obj):
        obj.resident = self.context['request'].user
        return super().save_object(obj)
