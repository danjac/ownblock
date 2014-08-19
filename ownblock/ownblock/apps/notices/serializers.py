from django.utils.functional import cached_property

from rest_framework import serializers

from guardian.shortcuts import get_objects_for_user

from apps.accounts.serializers.related import UserRelatedField

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    author = UserRelatedField(read_only=True)
    is_editable = serializers.SerializerMethodField('get_obj_perms')

    class Meta:
        model = Notice
        fields = (
            'id',
            'author',
            'title',
            'details',
            'created',
            'is_editable',
        )

    @cached_property
    def user_perms(self):
        return get_objects_for_user(self.context['request'].user, (
                                    'notices.change_notice',
                                    'notices.delete_notice'))

    def get_obj_perms(self, obj):
        return obj in self.user_perms
