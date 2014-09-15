
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
                       # Front page
                       url(r'', include('ownblock.apps.site.urls')),
                       # REST API
                       url(r'^api/users/', include(
                           'ownblock.apps.accounts.urls')),
                       url(r'^api/notices/', include(
                           'ownblock.apps.notices.urls')),
                       url(r'^api/amenities/', include(
                           'ownblock.apps.amenities.urls')),
                       url(r'^api/complaints/', include(
                           'ownblock.apps.complaints.urls')),
                       url(r'^api/messages/', include(
                           'ownblock.apps.messaging.urls')),
                       url(r'^api/storage/', include(
                           'ownblock.apps.storage.urls')),
                       url(r'^api/buildings/', include(
                           'ownblock.apps.buildings.urls')),
                       url(r'^api/tickets/', include(
                           'ownblock.apps.tickets.urls')),
                       url(r'^api/documents/', include(
                           'ownblock.apps.documents.urls')),
                       url(r'^api/contacts/', include(
                           'ownblock.apps.contacts.urls')),
                       url(r'^api/parking/', include(
                           'ownblock.apps.parking.urls')),

                       url(r'^signup/', include(
                           'ownblock.apps.signups.urls', namespace='signups')),

                       # Admin site
                       url(r'^backend/', include(admin.site.urls)),

                       )
# Authentication
urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^account/login/$', 'login', name='login'),
    url(r'^account/logout/$', 'logout_then_login', name='logout'),
    url(r'^account/reset/$', 'password_reset'),
    url(r'^account/reset_done/$', 'password_reset_done',
        name='password_reset_done'),
    url(r'^account/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm',
        kwargs={
            'post_reset_redirect': settings.LOGIN_URL,
        }, name='password_reset_confirm'),
    url(r'^account/invite/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm',
        kwargs={
            'template_name': 'registration/invitation_confirm.html',
            'post_reset_redirect': settings.LOGIN_URL,
        }, name='invitation_confirm'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
