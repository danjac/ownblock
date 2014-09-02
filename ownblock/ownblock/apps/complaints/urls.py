from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'complaints', views.ComplaintViewSet)

urlpatterns = router.urls
