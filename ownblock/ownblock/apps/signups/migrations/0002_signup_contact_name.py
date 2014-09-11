# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='contact_name',
            field=models.CharField(default='unknown', max_length=80),
            preserve_default=False,
        ),
    ]
