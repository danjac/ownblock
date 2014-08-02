# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('contacts_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buildings.Building'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('contacts', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table('contacts_contact')


    models = {
        'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'default': "'FI'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['contacts']