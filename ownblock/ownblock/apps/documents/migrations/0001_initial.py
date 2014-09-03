# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
import ownblock.apps.documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=ownblock.apps.documents.models._upload_to)),
                ('building', models.ForeignKey(to='buildings.Building')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
