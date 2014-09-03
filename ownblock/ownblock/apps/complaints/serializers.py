from rest_framework import serializers


from ..accounts.serializers import UserSerializer
from ..buildings.serializers import ApartmentSerializer

from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):

    resident_detail = UserSerializer(source='resident', read_only=True)
    apartment_detail = ApartmentSerializer(source='apartment', read_only=True)

    class Meta:
        model = Complaint
        fields = (
            'id',
            'complaint',
            'created',
            'resident',
            'resident_detail',
            'apartment',
            'apartment_detail',
        )
        read_only_fields = ('resident', )

    def validate_apartment(self, attrs, source):
        apartment = attrs[source]
        if apartment is None:
            return attrs
        if apartment.building != self.context['request'].building:
            raise serializers.ValidationError(
                "Apartment does not belong to building")
        return attrs
