# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.organization'
        db.delete_column('accounts_user', 'organization_id')

        # Adding field 'User.site'
        db.add_column('accounts_user', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sites.Site'], blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'User.organization'
        db.add_column('accounts_user', 'organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['organizations.Organization'], blank=True),
                      keep_default=False)

        # Deleting field 'User.site'
        db.delete_column('accounts_user', 'site_id')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['buildings.Apartment']", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '160', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'original_email': ('django.db.models.fields.EmailField', [], {'max_length': '160', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'resident'", 'max_length': '10'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['sites.Site']", 'blank': 'True'})
        },
        'buildings.apartment': {
            'Meta': {'object_name': 'Apartment', 'unique_together': "(('building', 'number'),)"},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_rooms': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'owner_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'})
        },
        'buildings.building': {
            'Meta': {'object_name': 'Building', 'unique_together': "(('address_1', 'address_2', 'city', 'postcode', 'country'),)"},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'FI'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'num_floors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['accounts']