from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'description',
            'email',
            'phone',
            'address',
        )

    def save_object(self, obj, **kwargs):
        obj.building = self.context['request'].building
        return super().save_object(obj, **kwargs)
