
def get_building(request):
    """Get building in request : for residents will depend on their
    apartment, for managers depends on the session"""

    if not request.user.is_authenticated():
        return None

    if request.user.apartment:
        return request.user.apartment.building

    if request.user.site:
        if 'building_id' in request.session:
            return request.user.site.building_set.get(
                pk=request.session['building_id']
            )
        buildings = request.user.site.building_set.all()
        if buildings:
            # by default, just pick the first one
            building = buildings[0]
            request.session['building_id'] = building.id
            return building

    return None
