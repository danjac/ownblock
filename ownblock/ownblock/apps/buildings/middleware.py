from django.utils.functional import SimpleLazyObject


def get_building(request):
    if not request.user.is_authenticated():
        return None

    if request.user.apartment:
        return request.user.apartment.building

    if request.user.organization and 'building_id' in request.session:
        return request.user.organization.building_set.get(
            request.session['building_id']
        )
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
