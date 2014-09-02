from rest_framework import serializers


from apps.accounts.serializers import UserSerializer
from apps.buidlings.serializers import ApartmentSerializer

from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):

    resident_detail = UserSerializer(source='resident', read_only=True)
    apartment_detail = ApartmentSerializer(source='apartment', read_only=True)

    class Meta:
        model = Complaint
        fields = (
            'id',
            'complaint',
            'resident',
            'resident_detail',
            'apartment',
            'apartment_detail',
        )
