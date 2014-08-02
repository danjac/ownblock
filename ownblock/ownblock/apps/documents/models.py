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
