from rest_framework import viewsets

from .models import Notice
from .serializers import NoticeSerializer


class NoticeViewSet(viewsets.ModelViewSet):

    model = Notice
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('-created')
