from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url('$', views.AuthView.as_view(),
                           name='authenticate')
                       )
