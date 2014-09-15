from django.conf import settings


def sites(request):
    """
    Lists URLs of sites
    """

    return {'sites': settings.SITE_URLS}
