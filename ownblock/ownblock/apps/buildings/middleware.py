from django.utils.functional import SimpleLazyObject

from . import get_building


class CurrentBuildingMiddleware(object):

    """Selects the current building. In the case of residents this
    will depend on their apartment; in the case of managers the building
    ID should be in the session. In other cases this will be None. The value
    is assigned to `request.building`.

    Ensure that this is added after AuthenticationMiddleware.
    """

    def process_request(self, request):
        request.building = SimpleLazyObject(lambda: get_building(request))
