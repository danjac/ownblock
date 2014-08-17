from rest_framework import viewsets


from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):

    model = Vehicle
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            resident__apartment__building=self.request.building
        ).select_related('resident',
                         'resident__apartment',)
