# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
