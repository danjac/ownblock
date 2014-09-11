# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ownblock.apps.storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_item_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, upload_to=ownblock.apps.storage.models._upload_image_to, null=True),
        ),
    ]
