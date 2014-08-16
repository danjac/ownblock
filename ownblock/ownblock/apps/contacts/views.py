from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManagerReadOnly

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):

    model = Contact
    serializer_class = ContactSerializer
    permission_classes = (IsResidentOrManagerReadOnly, )

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('name')
