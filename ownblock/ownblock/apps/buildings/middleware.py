from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.functional import SimpleLazyObject
from django.contrib.sites.models import Site, get_current_site

from . import get_building


class CurrentSiteMiddleware(object):

    """Gets current Site based on HTTP HOST (fallback on SITE_ID).

    Checks site against logged in user's site (depending on current building).
    If not matched then redirects user to default site (index page or
    admin if a staff member).

    The site object is added to request.site.

    This middleware goes after CurrentBuildingMiddleware
    """

    def get_site(self, request):

        try:
            return Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            return get_current_site(request)

    def get_redirect_url(self, request):
        scheme = 'https' if request.is_secure() else 'http'
        domain = request.site.domain
        path = None

        if request.building:
            domain = request.building.site.domain
            path = request.path

        elif request.user.staff:
            path = reverse('admin:index')

        else:
            path = reverse('index')

        return '%s://%s%s' % (scheme, domain, path)

    def process_request(self, request):
        request.site = SimpleLazyObject(lambda: self.get_site(request))
        if request.site is None or (
                request.building and request.building.site != request.site):
            return HttpResponseRedirect(self.get_redirect_url(request))
        return None


class CurrentBuildingMiddleware(object):

    """Selects the current building. In the case of residents this
    will depend on their apartment; in the case of managers the building
    ID should be in the session. In other cases this will be None. The value
    is assigned to `request.building`.

    Ensure that this is added after AuthenticationMiddleware.
    """

    def process_request(self, request):
        request.building = SimpleLazyObject(lambda: get_building(request))
