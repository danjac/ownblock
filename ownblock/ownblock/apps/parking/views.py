from rest_framework import viewsets


from .models import Vehicle
from .serializers import VehicleSerializer
from .permissions import IsOwnerOrManager


class VehicleViewSet(viewsets.ModelViewSet):

    model = Vehicle
    serializer_class = VehicleSerializer
    permission_classes = (IsOwnerOrManager,)

    def get_queryset(self):
        return super().get_queryset().filter(
            resident__apartment__building=self.request.building
        ).select_related('resident',
                         'resident__apartment',
                         'resident__apartment__building')
