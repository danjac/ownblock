# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Apartment.area'
        db.add_column('buildings_apartment', 'area',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Apartment.num_rooms'
        db.add_column('buildings_apartment', 'num_rooms',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Apartment', fields ['building', 'number']
        db.create_unique('buildings_apartment', ['building_id', 'number'])

        # Adding field 'Building.year'
        db.add_column('buildings_building', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Building.num_floors'
        db.add_column('buildings_building', 'num_floors',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Building', fields ['address_1', 'address_2', 'city', 'postcode', 'country']
        db.create_unique('buildings_building', ['address_1', 'address_2', 'city', 'postcode', 'country'])


    def backwards(self, orm):
        # Removing unique constraint on 'Building', fields ['address_1', 'address_2', 'city', 'postcode', 'country']
        db.delete_unique('buildings_building', ['address_1', 'address_2', 'city', 'postcode', 'country'])

        # Removing unique constraint on 'Apartment', fields ['building', 'number']
        db.delete_unique('buildings_apartment', ['building_id', 'number'])

        # Deleting field 'Apartment.area'
        db.delete_column('buildings_apartment', 'area')

        # Deleting field 'Apartment.num_rooms'
        db.delete_column('buildings_apartment', 'num_rooms')

        # Deleting field 'Building.year'
        db.delete_column('buildings_building', 'year')

        # Deleting field 'Building.num_floors'
        db.delete_column('buildings_building', 'num_floors')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'buildings.apartment': {
            'Meta': {'unique_together': "(('building', 'number'),)", 'object_name': 'Apartment'},
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
            'Meta': {'unique_together': "(('address_1', 'address_2', 'city', 'postcode', 'country'),)", 'object_name': 'Building'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'default': "'FI'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'num_floors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['buildings']