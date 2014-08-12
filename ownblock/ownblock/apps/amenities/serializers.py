from rest_framework import serializers

from .models import Amenity


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ('id', 'name', 'is_available')
