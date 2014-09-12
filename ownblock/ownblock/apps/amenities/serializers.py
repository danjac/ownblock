from django.db.models.query import Q
from django.utils import timezone

from rest_framework import serializers

from ..accounts.serializers import UserSerializer

from .models import Amenity, Booking


class AmenityRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            'id': value.id,
            'name': value.name,
        }


class BookingSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)
    amenity_detail = AmenityRelatedField('amenity', read_only=True)

    is_editable = serializers.SerializerMethodField('is_obj_editable')
    is_removable = serializers.SerializerMethodField('is_obj_removable')

    class Meta:
        model = Booking
        fields = ('id',
                  'resident',
                  'amenity',
                  'amenity_detail',
                  'reserved_from',
                  'reserved_to',
                  'is_editable',
                  'is_removable')

    def is_obj_editable(self, obj):
        return obj.has_permission(self.context['request'].user,
                                  'amenities.change_booking')

    def is_obj_removable(self, obj):
        return obj.has_permission(self.context['request'].user,
                                  'amenities.delete_booking')

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
            raise serializers.ValidationError("'From' date must be in future")
        return attrs

    def validate(self, attrs):
        if attrs['reserved_from'] > attrs['reserved_to']:
            raise serializers.ValidationError(
                "The 'from' date is after the 'to' date")
        bookings = attrs['amenity'].booking_set.all()
        date_range = (attrs['reserved_from'], attrs['reserved_to'])
        qs = bookings.filter(
            Q(reserved_from__range=date_range) |
            Q(reserved_to__range=date_range))

        booking_id = self.init_data.get('id')
        if booking_id:
            qs = qs.exclude(pk=booking_id)
        if qs.exists():
            raise serializers.ValidationError("Booking conflict")

        return attrs


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ('id', 'name', 'is_available', )
