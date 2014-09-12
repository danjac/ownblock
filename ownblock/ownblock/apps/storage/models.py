import uuid
import os
import mimetypes

from django.conf import settings
from django.db import models

from sorl.thumbnail import get_thumbnail, delete


from ..buildings.models import Building


class Place(models.Model):

    name = models.CharField(max_length=60)
    location = models.TextField(blank=True)
    building = models.ForeignKey(Building)

    def __str__(self):
        return self.name

    def has_permission(self, user, perm):
        return (user.role == 'manager' and
                user.site_id == self.building.site_id)


def _upload_image_to(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = uuid.uuid4().hex + ext
    return "storage/{}/{}".format(instance.place_id, filename)


class Item(models.Model):

    description = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=30, blank=True)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL)
    place = models.ForeignKey(Place)
    photo = models.ImageField(
        upload_to=_upload_image_to, null=True, blank=True)

    def __str__(self):
        return self.description

    def has_permission(self, user, perm):
        if user.role == 'resident':
            return self.resident == user
        if user.role == 'manager':
            return self.place.building.site_id == user.site_id
        return False

    def get_photo_content_type(self):
        if not self.photo:
            return None
        return mimetypes.guess_type(self.photo.name)[0]

    @models.permalink
    def get_photo_url(self):
        return ('item-photo', [self.pk])

    @models.permalink
    def get_thumbnail_url(self):
        return ('item-thumbnail', [self.pk])

    def get_thumbnail(self):
        if not self.photo:
            return None
        return get_thumbnail(self.photo.file,
                             '150x150',
                             crop='center',
                             quality=99)

    def delete_photo(self):
        delete(self.photo)
        self.photo = ""
        self.save()
