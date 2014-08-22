# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Organization.group'
        db.delete_column('organizations_organization', 'group_id')


    def backwards(self, orm):
        # Adding field 'Organization.group'
        db.add_column('organizations_organization', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['auth.Group']),
                      keep_default=False)


    models = {
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['organizations']