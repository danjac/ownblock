from django.utils.functional import cached_property

from rest_framework import serializers

from guardian.shortcuts import get_objects_for_user

from apps.accounts.serializers import UserSerializer

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)
    is_editable = serializers.SerializerMethodField('get_obj_perms')

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
        if obj.resident is None:
            obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)

    @cached_property
    def user_perms(self):
        return get_objects_for_user(self.context['request'].user, (
                                    'parking.change_vehicle',
                                    'parking.delete_vehicle'))

    def get_obj_perms(self, obj):
        return obj in self.user_perms
