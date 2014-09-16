from django.conf.urls import patterns, url

from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'buildings', views.BuildingViewSet)
router.register(r'apartments', views.ApartmentViewSet)

urlpatterns = router.urls

urlpatterns += patterns('',
                        url('^timeline$', views.TimelineView.as_view(),
                            name='timeline')
                        )
