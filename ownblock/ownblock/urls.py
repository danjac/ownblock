import json
import logging

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, get_current_site

from apps.accounts.serializers import AuthUserSerializer

admin.autodiscover()


class AppView(TemplateView):
    template_name = 'app.html'
	
    def get_current_site(self):
        try:
           return Site.objects.get(domain=self.request.get_host())
        except Site.DoesNotExist:
           return get_current_site(self.request)

    def get(self, request, *args, **kwargs):
        """Ensure the user has access here"""

        self.site = self.get_current_site()
        logging.error("SITE %s", self.site)

        user_site = None

        if self.request.user.site_id:
            user_site = self.request.user.site

        elif self.request.user.apartment_id:
            user_site = self.request.user.apartment.building.site

        redirect_url = None

        if user_site is None:
            if self.request.user.is_staff:
                redirect_url = reverse('admin:index')
            else:
                redirect_url = reverse('index')
        elif user_site != self.site:
            scheme = 'https' if request.is_secure() else 'http'
            redirect_url = '%s://%s%s' % (scheme,
                                          user_site.domain,
                                          request.path)

        if redirect_url:
            return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # bootstrap data
        context['user_data'] = json.dumps(
            AuthUserSerializer(self.request.user,
                               context={'request': self.request}).data
        )
        context['site'] = self.site
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
