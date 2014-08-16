from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'description',
            'registration_number',
            'reserved_place',
            'resident',
        )

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)
