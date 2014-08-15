
from rest_framework import serializers


class UserRelatedField(serializers.RelatedField):

    def to_native(self, value):
        return {
            "id": value.id,
            "name": value.get_short_name(),
            "full_name": value.get_full_name(),
        }
