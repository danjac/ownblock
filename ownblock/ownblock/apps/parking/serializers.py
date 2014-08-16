from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)
    is_editable = serializers.SerializerMethodField('can_edit_or_delete')

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'description',
            'registration_number',
            'reserved_place',
            'resident',
            'is_editable',
        )

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)

    def can_edit_or_delete(self, obj):
        return obj.can_edit_or_delete(self.context['request'].user)
