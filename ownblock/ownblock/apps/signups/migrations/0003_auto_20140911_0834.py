# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('signups', '0002_signup_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='is_nonprofit',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signup',
            name='domain',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator(re.compile('^([\\w]+)$', 32), 'Not a valid domain')], max_length=30),
        ),
    ]
