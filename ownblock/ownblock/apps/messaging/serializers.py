from rest_framework import serializers

from ..accounts.serializers import UserSerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(source='sender', read_only=True)
    recipient_detail = UserSerializer(source='recipient', read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'sender',
            'recipient',
            'recipient_detail',
            'header',
            'details',
            'is_read',
            'parent',
            'created',
        )

        read_only_fields = ('is_read', 'created',)

    def validate_recipient(self, attrs, source):
        recipient = attrs[source]

        if (recipient.apartment and
                recipient.apartment.building !=
                self.context['request'].building):
            raise serializers.ValidationError("Recipient does not live here")

        elif (recipient.site and
              recipient.site != self.context['request'].building.site):
                raise serializers.ValidationError(
                    'Recipient is not associated with this building')

        if recipient == self.context['request'].user:
            raise serializers.ValidationError(
                "You can't send message to yourself"
            )
        return attrs
