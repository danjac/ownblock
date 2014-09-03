from rest_framework import serializers

from ..accounts.serializers.related import UserRelatedField

from .models import Place, Item


class PlaceSerializer(serializers.ModelSerializer):

    is_editable = serializers.SerializerMethodField('is_obj_editable')
    is_removable = serializers.SerializerMethodField('is_obj_removable')

    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'is_editable',
            'is_removable',
        )

    def _has_permission(self, obj, perm):
        return obj.has_permission(self.context['request'].user, perm)

    def is_obj_editable(self, obj):
        return self._has_permission(obj, 'storage.change_place')

    def is_obj_removable(self, obj):
        return self._has_permission(obj, 'storage.delete_place')


class ItemSerializer(serializers.ModelSerializer):

    resident = UserRelatedField(read_only=True)
    place_name = serializers.SerializerMethodField('get_place_name')
    apartment = serializers.SerializerMethodField('get_apartment')
    is_editable = serializers.SerializerMethodField('is_obj_editable')
    is_removable = serializers.SerializerMethodField('is_obj_removable')

    class Meta:
        model = Item
        fields = ('id',
                  'place',
                  'place_name',
                  'resident',
                  'description',
                  'apartment',
                  'is_editable',
                  'is_removable',
                  'serial_no')

    def get_place_name(self, obj):
        return obj.place.name

    def get_apartment(self, obj):
        return {'id': obj.resident.apartment_id,
                'number': obj.resident.apartment.number}

    def validate_place(self, attrs, source):
        value = attrs[source]
        if value.building != self.context['request'].building:
            raise serializers.ValidationError("Place not found")
        return attrs

    def _has_permission(self, obj, perm):
        return obj.has_permission(self.context['request'].user, perm)

    def is_obj_editable(self, obj):
        return self._has_permission(obj, 'storage.change_item')

    def is_obj_removable(self, obj):
        return self._has_permission(obj, 'storage.delete_item')
