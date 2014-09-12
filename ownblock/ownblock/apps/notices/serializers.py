from rest_framework import serializers

from ..accounts.serializers import UserSerializer

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    is_editable = serializers.SerializerMethodField('is_obj_editable')
    is_removable = serializers.SerializerMethodField('is_obj_removable')

    class Meta:
        model = Notice
        fields = (
            'id',
            'author',
            'title',
            'details',
            'created',
            'is_editable',
            'is_removable',
        )

    def _has_permission(self, obj, perm):
        return obj.has_permission(self.context['request'].user, perm)

    def is_obj_editable(self, obj):
        return self._has_permission(obj, 'notices.change_notice')

    def is_obj_removable(self, obj):
        return self._has_permission(obj, 'notices.delete_notice')
