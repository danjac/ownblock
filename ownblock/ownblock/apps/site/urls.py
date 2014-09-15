from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap

from . import views, sitemaps

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(
                           template_name='index.html'),
                           name='index'),

                       url(r'^about$', TemplateView.as_view(
                           template_name='about.html'),
                           name='about'),

                       url(r'^pricing$', TemplateView.as_view(
                           template_name='pricing.html'),
                           name='pricing'),


                       url(r'^contact$',
                           views.ContactView.as_view(), name='contact'),

                       # Application container
                       url(r'^app$', login_required(
                           views.AppView.as_view()),
                           name='app'),

                       # Sitemaps
                       url(r'^sitemap\.xml$', sitemap,
                           {'sitemaps': sitemaps.sitemaps},
                           name='django.contrib.sitemaps.views.sitemap'),

                       )
