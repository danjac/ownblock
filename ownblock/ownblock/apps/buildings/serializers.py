from rest_framework import serializers

from apps.accounts.serializers import UserRelatedField

from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):

    user_set = UserRelatedField(many=True)

    class Meta:
        model = Apartment
        fields = ('id', 'number', 'floor', 'user_set')
