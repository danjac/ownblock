import mimetypes
import os

from django.db import models

from model_utils.models import TimeStampedModel

from apps.buildings.models import Building


class Document(TimeStampedModel):

    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=lambda obj, filename:
                            "docs/%s/%s" % (obj.building_id, filename))

    building = models.ForeignKey(Building)

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
