# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signups', '0003_auto_20140911_0834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='is_nonprofit',
        ),
    ]
