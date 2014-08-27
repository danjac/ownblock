from rest_framework import serializers

from .models import Ticket


class ResidentTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            'id',
            'description',
            'status',
            'created',
        )
