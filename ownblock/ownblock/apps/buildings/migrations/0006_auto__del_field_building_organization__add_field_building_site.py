# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Building.organization'
        db.delete_column('buildings_building', 'organization_id')

        # Adding field 'Building.site'
        db.add_column('buildings_building', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Building.organization'
        db.add_column('buildings_building', 'organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'], default=1),
                      keep_default=False)

        # Deleting field 'Building.site'
        db.delete_column('buildings_building', 'site_id')


    models = {
        'buildings.apartment': {
            'Meta': {'unique_together': "(('building', 'number'),)", 'object_name': 'Apartment'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_rooms': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '60'}),
            'owner_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '12'})
        },
        'buildings.building': {
            'Meta': {'unique_together': "(('address_1', 'address_2', 'city', 'postcode', 'country'),)", 'object_name': 'Building'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'default': "'FI'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'num_floors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['buildings']