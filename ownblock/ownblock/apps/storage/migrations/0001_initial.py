# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table('storage_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buildings.Building'])),
        ))
        db.send_create_signal('storage', ['Place'])

        # Adding model 'Item'
        db.create_table('storage_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('serial_no', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('resident', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Place'])),
        ))
        db.send_create_signal('storage', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table('storage_place')

        # Deleting model 'Item'
        db.delete_table('storage_item')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['buildings.Apartment']"}),
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['buildings.Building']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '160', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'resident'"})
        },
        'buildings.apartment': {
            'Meta': {'object_name': 'Apartment'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'owner_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'})
        },
        'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'default': "'FI'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'storage.item': {
            'Meta': {'object_name': 'Item'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Place']"}),
            'resident': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'storage.place': {
            'Meta': {'object_name': 'Place'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['storage']