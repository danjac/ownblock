from django.utils.functional import SimpleLazyObject
from django.contrib.sites.models import Site, get_current_site

from . import get_building


class CurrentSiteMiddleware(object):

    """Gets current Site based on HTTP HOST (fallback on SITE_ID).

    The site object is added to request.site.
    """

    def get_site(self, request):

        try:
            return Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            return get_current_site(request)

    def process_request(self, request):
        request.site = SimpleLazyObject(lambda: self.get_site(request))


class CurrentBuildingMiddleware(object):

    """Selects the current building. In the case of residents this
    will depend on their apartment; in the case of managers the building
    ID should be in the session. In other cases this will be None. The value
    is assigned to `request.building`.

    Ensure that this is added after AuthenticationMiddleware.
    """

    def process_request(self, request):
        request.building = SimpleLazyObject(lambda: get_building(request))
