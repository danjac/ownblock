import json

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from apps.accounts.serializers import AuthUserSerializer

admin.autodiscover()


class AppView(TemplateView):
    template_name = 'app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # bootstrap data
        context['user_data'] = json.dumps(
            AuthUserSerializer(self.request.user,
                               context={'request': self.request}).data
        )
        return context


urlpatterns = patterns('',
                       # Front page
                       url(r'^$', TemplateView.as_view(
                           template_name='index.html'),
                           name='index'),

                       # Application container
                       url(r'^app$', login_required(AppView.as_view()),
                           name='app'),

                       # REST API
                       url(r'^api/users/', include('apps.accounts.urls')),
                       url(r'^api/notices/', include('apps.notices.urls')),
                       url(r'^api/amenities/', include('apps.amenities.urls')),
                       url(r'^api/messages/', include('apps.messaging.urls')),
                       url(r'^api/storage/', include('apps.storage.urls')),
                       url(r'^api/buildings/', include('apps.buildings.urls')),
                       url(r'^api/documents/', include('apps.documents.urls')),
                       url(r'^api/contacts/', include('apps.contacts.urls')),
                       url(r'^api/parking/', include('apps.parking.urls')),


                       # Admin site
                       url(r'^admin/', include(admin.site.urls)),
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
