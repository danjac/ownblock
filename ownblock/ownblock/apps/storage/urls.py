from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'places', views.PlaceViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = router.urls
