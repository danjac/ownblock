from rest_framework import viewsets

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):

    model = Contact
    serializer_class = ContactSerializer

    def pre_save(self, obj):
        obj.building = self.request.building

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('name')
