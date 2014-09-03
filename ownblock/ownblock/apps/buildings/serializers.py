from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Apartment, Building


class ApartmentRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            'id': value.id,
            'floor': value.floor,
            'number': value.number,
            'name': "%s / Floor %d" % (value.number, value.floor),
        }


class ResidentSerializer(serializers.ModelSerializer):

    """Specifically to add new residents to apartment"""

    full_name = serializers.SerializerMethodField('get_full_name')
    gravatar = serializers.SerializerMethodField('get_gravatar_url')

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'full_name',
            'gravatar',
            'is_active',
        )

    def __init__(self, apartment, *args, **kwargs):
        self.apartment = apartment
        super().__init__(*args, **kwargs)

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_gravatar_url(self, obj):
        return obj.get_gravatar_url(size=25)


class BuildingSerializer(serializers.ModelSerializer):

    full_address = serializers.SerializerMethodField('get_full_address')

    class Meta:
        model = Building
        fields = ('id',
                  'full_address',
                  'address_1',
                  'address_2',
                  'year',
                  'num_floors',
                  'city',
                  'postcode',
                  'latitude',
                  'longitude')

    def get_full_address(self, obj):
        return obj.get_full_address()


class ApartmentSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Apartment
        fields = ('id',
                  'number',
                  'floor',
                  'area',
                  'name',
                  'num_rooms')

    def get_name(self, obj):
        return "%s / Floor %d" % (obj.number, obj.floor)
