from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.CreateSignup.as_view(), name='signup'),
                       url(r'done$',
                           views.SignupDone.as_view(), name='done')
                       )
