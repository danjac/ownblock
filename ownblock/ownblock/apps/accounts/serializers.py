from rest_framework import serializers

from .models import User


class UserRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            "id": value.id,
            "name": value.get_short_name(),
            "full_name": value.get_full_name(),
        }


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = User

        fields = (
            'id',
            'first_name',
            'last_name',
            'role',
            'apartment',
            'full_name',
        )

        read_only_fields = ('role', )

    def get_full_name(self, obj):
        return obj.get_full_name()


class AuthUserSerializer(UserSerializer):

    """Current authenticated user"""

    building = serializers.SerializerMethodField('get_building')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('building',)

    def get_building(self, obj):
        if 'request' in self.context:
            building = self.context['request'].building
            if building:
                return {
                    'id': building.id,
                    'full_address': building.get_full_address(),
                    'latitude': building.latitude,
                    'longitude': building.longitude,
                }
        return None
