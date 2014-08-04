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
        )
