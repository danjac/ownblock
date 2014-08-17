from django.utils.functional import cached_property

from rest_framework import serializers

from guardian.shortcuts import get_objects_for_user

from apps.accounts.serializers.related import UserRelatedField

from .models import Place, Item


class PlaceSerializer(serializers.ModelSerializer):

    is_editable = serializers.SerializerMethodField('get_obj_perms')

    class Meta:
        model = Place
        fields = ('id', 'name', 'is_editable')

    def save_object(self, obj, *args, **kwargs):
        obj.building = self.context['request'].building
        return super().save_object(obj, *args, **kwargs)

    @cached_property
    def user_perms(self):
        return get_objects_for_user(self.context['request'].user, (
                                    'storage.change_place',
                                    'storage.delete_place'))

    def get_obj_perms(self, obj):
        return obj in self.user_perms


class ItemSerializer(serializers.ModelSerializer):

    resident = UserRelatedField(read_only=True)
    place_name = serializers.SerializerMethodField('get_place_name')
    apartment = serializers.SerializerMethodField('get_apartment')
    is_editable = serializers.SerializerMethodField('get_obj_perms')

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

    def validate_place(self, attrs, source):
        value = attrs[source]
        if value.building != self.context['request'].building:
            raise serializers.ValidationError("Place not found")
        return attrs

    @cached_property
    def user_perms(self):
        return get_objects_for_user(self.context['request'].user, (
                                    'storage.change_item',
                                    'storage.delete_item'))

    def get_obj_perms(self, obj):
        return obj in self.user_perms

    def save_object(self, obj, *args, **kwargs):
        obj.resident = self.context['request'].user
        return super().save_object(obj, *args, **kwargs)
