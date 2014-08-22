from rest_framework import serializers

from apps.buildings.serializers import (
    BuildingSerializer,
    ApartmentRelatedField
)

from ..models import User


class UserSerializer(serializers.ModelSerializer):

    apartment_detail = ApartmentRelatedField(source='apartment')
    full_name = serializers.SerializerMethodField('get_full_name')

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
        )

        read_only_fields = ('role', )

    def get_full_name(self, obj):
        return obj.get_full_name()


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
        fields = UserSerializer.Meta.fields + ('building', 'email')

    def get_building(self, obj):
        if 'request' in self.context:
            building = self.context['request'].building
            if building:
                return BuildingSerializer().to_native(building)
            return None
