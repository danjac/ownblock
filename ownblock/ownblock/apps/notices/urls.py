from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'notices', views.NoticeViewSet)

urlpatterns = router.urls
