# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ownblock.apps.storage.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_place_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=ownblock.apps.storage.models._upload_image_to),
            preserve_default=True,
        ),
    ]
