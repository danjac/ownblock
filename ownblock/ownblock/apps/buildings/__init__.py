
def get_building(request):
    """Get building in request : for residents will depend on their
    apartment, for managers depends on the session"""

    if not request.user.is_authenticated():
        return None

    if request.user.apartment:
        return request.user.apartment.building

    if request.user.organization and 'building_id' in request.session:
        return request.user.organization.building_set.get(
            request.session['building_id']
        )
    return None
