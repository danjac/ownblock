# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('messaging_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], related_name='sent_messages')),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], related_name='received_messages')),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['messaging.Message'], blank=True, null=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('messaging', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('messaging_message')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Apartment']", 'blank': 'True', 'null': 'True'}),
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['buildings.Building']"}),
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
        'messaging.message': {
            'Meta': {'object_name': 'Message'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.Message']", 'blank': 'True', 'null': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'related_name': "'received_messages'"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'related_name': "'sent_messages'"})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['messaging']