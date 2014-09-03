
from rest_framework import serializers

from ..accounts.serializers import UserSerializer

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)

    is_editable = serializers.SerializerMethodField('is_obj_editable')
    is_removable = serializers.SerializerMethodField('is_obj_removable')

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'description',
            'registration_number',
            'reserved_place',
            'resident',
            'is_editable',
            'is_removable',
        )

    def _has_permission(self, obj, perm):
        return obj.has_permission(self.context['request'].user, perm)

    def is_obj_editable(self, obj):
        return self._has_permission(obj, 'parking.change_vehicle')

    def is_obj_removable(self, obj):
        return self._has_permission(obj, 'parking.delete_vehicle')
