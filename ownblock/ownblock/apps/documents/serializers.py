from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    download_url = serializers.SerializerMethodField('get_download_url')

    class Meta:
        model = Document

        fields = (
            'id',
            'file',
            'title',
            'created',
            'download_url',
        )
        write_only_fields = ('file', )

    def get_download_url(self, obj):
        return obj.get_download_url()

    def save_object(self, obj, **kwargs):
        obj.building = self.context['request'].building
        return super().save_object(obj, **kwargs)
