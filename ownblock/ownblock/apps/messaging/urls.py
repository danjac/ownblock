from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'messages', views.MessageViewSet)
urlpatterns = router.urls
