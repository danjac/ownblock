from django.db.models.query import Q

from rest_framework import viewsets

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):

    model = Message
    serializer_class = MessageSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(recipient=self.request.user) |
            Q(sender=self.request.user)
        ).select_related('sender', 'recipient').order_by('-created')
