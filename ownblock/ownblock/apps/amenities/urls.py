from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'amenities', views.AmenityViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = router.urls
