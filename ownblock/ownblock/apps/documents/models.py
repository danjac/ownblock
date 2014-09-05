import mimetypes
import os

from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel

from ..buildings.models import Building


def _upload_to(instance, filename):
    return "docs/%s/%s" % (instance.building_id, filename)


class Document(TimeStampedModel):

    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=_upload_to)
    building = models.ForeignKey(Building)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_content_type(self):
        return mimetypes.guess_type(self.file.name)[0]

    def get_filename(self):
        return os.path.basename(self.file.name)

    @models.permalink
    def get_download_url(self):
        return ('document-download', [self.pk])

    def has_permission(self, user, perm):
        return (user.role == 'manager' and
                self.building.site_id == user.site_id)
