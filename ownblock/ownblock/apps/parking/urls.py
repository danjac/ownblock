from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'vehicles', views.VehicleViewSet)

urlpatterns = router.urls
