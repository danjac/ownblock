from rest_framework import viewsets

from .models import Notice
from .serializers import NoticeSerializer
from .permissions import IsAuthorOrManager


class NoticeViewSet(viewsets.ModelViewSet):

    model = Notice
    serializer_class = NoticeSerializer
    permission_classes = (IsAuthorOrManager, )

    def get_queryset(self):
        return super().get_queryset().filter(building=self.request.building)
