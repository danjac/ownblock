from rest_framework import serializers

from .models import User


class UserRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            "id": value.id,
            "name": value.get_short_name(),
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            'id',
            'first_name',
            'last_name',
            'role',
        )

        read_only_fields = ('role', )


class AuthUserSerializer(UserSerializer):

    """Current authenticated user"""

    building = serializers.SerializerMethodField('get_building')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('building',)

    def get_building(self, obj):
        if 'request' in self.context:
            building = self.context['request'].building
            if building is not None:
                return {
                    'id': building.id,
                    'full_address': building.get_full_address(),
                    'latitude': building.latitude,
                    'longitude': building.longitude,
                }
        return None
