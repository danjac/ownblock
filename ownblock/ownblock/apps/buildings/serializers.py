from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.accounts.serializers.related import UserRelatedField

from .models import Apartment, Building


class ApartmentRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            'id': value.id,
            'floor': value.floor,
            'number': value.number,
        }


class ResidentSerializer(serializers.ModelSerializer):

    """Specifically to add new residents to apartment"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'apartment',
        )


class BuildingSerializer(serializers.ModelSerializer):

    full_address = serializers.SerializerMethodField('get_full_address')

    class Meta:
        model = Building
        fields = ('id',
                  'full_address',
                  'address_1',
                  'address_2',
                  'city',
                  'postcode',
                  'latitude',
                  'longitude')

    def get_full_address(self, obj):
        return obj.get_full_address()


class ApartmentSerializer(serializers.ModelSerializer):

    user_set = UserRelatedField(many=True)

    class Meta:
        model = Apartment
        fields = ('id', 'number', 'floor', 'user_set')
