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
