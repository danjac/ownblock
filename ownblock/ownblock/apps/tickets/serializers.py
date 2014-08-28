from rest_framework import serializers

from .models import Ticket


from apps.accounts.serializers import UserSerializer
from apps.buildings.serializers import ApartmentRelatedField


class TicketSerializer(serializers.ModelSerializer):

    reporter_detail = UserSerializer(source='reporter', read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'description',
            'status',
            'created',
            'reporter',
            'reporter_detail',
        )

        read_only_fields = ('reporter',)


class ManagerTicketSerializer(TicketSerializer):

    apartment_detail = ApartmentRelatedField(
        source='apartment', read_only=True)

    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields + (
            'apartment',
            'apartment_detail',
        )
