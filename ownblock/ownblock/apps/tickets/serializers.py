from rest_framework import serializers


from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            'id',
            'description',
            'status',
            'created',
        )
