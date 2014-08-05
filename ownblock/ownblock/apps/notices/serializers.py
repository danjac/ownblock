from rest_framework import serializers

from apps.accounts.serializers import UserRelatedField

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    author = UserRelatedField(read_only=True)

    class Meta:
        model = Notice
        fields = (
            'id',
            'author',
            'title',
            'details',
            'created',
        )

    def save_object(self, obj, *args, **kwargs):
        request = self.context['request']
        obj.author = request.user
        obj.building = request.building
        super(NoticeSerializer, self).save_object(obj, *args, **kwargs)
