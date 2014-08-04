from rest_framework import viewsets

from apps.accounts.permissions import IsResidentOrManager

from .models import Notice
from .serializers import NoticeSerializer


class NoticeViewSet(viewsets.ModelViewSet):

    model = Notice
    serializer_class = NoticeSerializer
    permission_classes = (IsResidentOrManager, )

    def get_queryset(self):
        return super().get_queryset().filter(building=self.request.building)
