from django.conf.urls import patterns, url

from rest_framework import routers

from . import views

urlpatterns = patterns('',
                       url('^auth$', views.AuthView.as_view(),
                           name='authenticate')
                       )

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'people', views.UserViewSet)
urlpatterns += router.urls
