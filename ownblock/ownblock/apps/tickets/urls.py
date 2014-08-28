from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('residents', views.ResidentTicketViewSet)
router.register('managers', views.ManagerTicketViewSet)
urlpatterns = router.urls
