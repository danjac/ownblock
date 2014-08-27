from rest_framework import serializers


from apps.amenities.serializers import AmenityRelatedField
from apps.buildings.serializers import ApartmentRelatedField
from apps.accounts.serializers.related import UserRelatedField

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    amenity = AmenityRelatedField()
    apartment = ApartmentRelatedField()
    reporter = UserRelatedField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'description',
            'status',
            'created',
            'amenity',
            'apartment',
            'reporter',
        )
