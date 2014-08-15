from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    download_url = serializers.SerializerMethodField('get_download_url')

    class Meta:
        model = Document

        fields = (
            'id',
            'title',
            'created',
            'download_url',
        )

    def get_download_url(self, obj):
        return obj.get_download_url()
