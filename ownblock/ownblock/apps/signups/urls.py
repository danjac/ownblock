from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CreateSignup.as_view(), name='signup'),
                       url(r'done/(?P<pk>[0-9]+)$',
                           views.SignupDone.as_view(), name='done')
                       )
