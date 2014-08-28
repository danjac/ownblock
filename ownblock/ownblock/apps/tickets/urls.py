from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tickets', views.TicketViewSet)
urlpatterns = router.urls
