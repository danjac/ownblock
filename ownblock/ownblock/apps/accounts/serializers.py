from rest_framework import serializers

from ..buildings.serializers import (
    BuildingSerializer,
    ApartmentRelatedField
)

from .models import User


class UserSerializer(serializers.ModelSerializer):

    apartment_detail = ApartmentRelatedField(source='apartment')
    full_name = serializers.SerializerMethodField('get_full_name')
    gravatar = serializers.SerializerMethodField('get_gravatar_url')

    class Meta:
        model = User

        fields = (
            'id',
            'first_name',
            'last_name',
            'role',
            'apartment',
            'apartment_detail',
            'full_name',
            'is_active',
            'gravatar',
        )

        read_only_fields = ('role', )

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_gravatar_url(self, obj):
        return obj.get_gravatar_url(size=25)


class RestrictedUserSerializer(UserSerializer):

    """Accessible only to managers"""

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'email',
            'phone',
        )


class AuthUserSerializer(UserSerializer):

    """Current authenticated user"""

    building = serializers.SerializerMethodField('get_building')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'building',
            'email',
            'phone'
        )

    def get_building(self, obj):
        if 'request' in self.context:
            building = self.context['request'].building
            if building:
                return BuildingSerializer().to_native(building)
            return None
