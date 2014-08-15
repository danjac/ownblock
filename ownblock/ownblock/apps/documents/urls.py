from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = router.urls
