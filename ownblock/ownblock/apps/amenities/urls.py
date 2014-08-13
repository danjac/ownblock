from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bookings', views.BookingViewSet)
router.register(r'items', views.AmenityViewSet)

urlpatterns = router.urls
