from rest_framework import serializers

from apps.accounts.serializers.related import UserRelatedField

from .models import Place, Item


class PlaceSerializer(serializers.ModelSerializer):

    is_editable = serializers.SerializerMethodField(
        'can_edit_or_delete'
    )

    class Meta:
        model = Place
        fields = ('id', 'name', 'is_editable')

    def save_object(self, obj, *args, **kwargs):
        obj.building = self.context['request'].building
        return super().save_object(obj, *args, **kwargs)

    def can_edit_or_delete(self, obj):
        return obj.can_edit_or_delete(self.context['request'].user)


class ItemSerializer(serializers.ModelSerializer):

    resident = UserRelatedField(read_only=True)
    place_name = serializers.SerializerMethodField('get_place_name')
    apartment = serializers.SerializerMethodField('get_apartment')
    is_editable = serializers.SerializerMethodField(
        'can_edit_or_delete'
    )

    class Meta:
        model = Item
        fields = ('id',
                  'place',
                  'place_name',
                  'resident',
                  'description',
                  'apartment',
                  'is_editable',
                  'serial_no')

    def get_place_name(self, obj):
        return obj.place.name

    def get_apartment(self, obj):
        return obj.resident.apartment.number

    def can_edit_or_delete(self, obj):
        return obj.can_edit_or_delete(self.context['request'].user)

    def validate_place(self, attrs, source):
        value = attrs[source]
        if value.building != self.context['request'].building:
            raise serializers.ValidationError("Place not found")
        return attrs

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)
