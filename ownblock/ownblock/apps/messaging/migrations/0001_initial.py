# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('header', models.CharField(max_length=200)),
                ('details', models.TextField(blank=True)),
                ('is_read', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, to='messaging.Message')),
                ('recipient', models.ForeignKey(related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
