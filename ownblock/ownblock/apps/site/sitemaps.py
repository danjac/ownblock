from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap


class MainSitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['index', 'about', 'contact', 'pricing']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'main': MainSitemap,
}
