from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(
                           template_name='index.html')),

                       # REST API
                       url(r'^api/users/', include('apps.accounts.urls')),
                       url(r'^api/notices/', include('apps.notices.urls')),
                       url(r'^api/amenities/', include('apps.amenities.urls')),
                       url(r'^api/messages/', include('apps.messaging.urls')),

                       # Admin site
                       url(r'^admin/', include(admin.site.urls)),
                       )

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
