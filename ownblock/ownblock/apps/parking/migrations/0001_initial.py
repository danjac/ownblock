# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vehicle'
        db.create_table('parking_vehicle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('registration_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('country', self.gf('django_countries.fields.CountryField')(default='FI', max_length=2)),
            ('resident', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('reserved_place', self.gf('django.db.models.fields.CharField')(blank=True, max_length=12)),
        ))
        db.send_create_signal('parking', ['Vehicle'])


    def backwards(self, orm):
        # Deleting model 'Vehicle'
        db.delete_table('parking_vehicle')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['buildings.Apartment']", 'null': 'True'}),
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['buildings.Building']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '160', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'resident'", 'max_length': '10'})
        },
        'buildings.apartment': {
            'Meta': {'object_name': 'Apartment'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '60'}),
            'owner_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '12'})
        },
        'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'FI'", 'max_length': '2'}),
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
        'parking.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'country': ('django_countries.fields.CountryField', [], {'default': "'FI'", 'max_length': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'reserved_place': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '12'}),
            'resident': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"})
        }
    }

    complete_apps = ['parking']