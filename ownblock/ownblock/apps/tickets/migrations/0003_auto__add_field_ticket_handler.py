# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Ticket.handler'
        db.add_column('tickets_ticket', 'handler',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='handled_tickets', null=True, to=orm['accounts.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Ticket.handler'
        db.delete_column('tickets_ticket', 'handler_id')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['buildings.Apartment']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '160', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'original_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '160'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'resident'", 'max_length': '10'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['sites.Site']"})
        },
        'amenities.amenity': {
            'Meta': {'object_name': 'Amenity'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'buildings.apartment': {
            'Meta': {'object_name': 'Apartment', 'unique_together': "(('building', 'number'),)"},
            'area': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_rooms': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '60'}),
            'owner_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '12'})
        },
        'buildings.building': {
            'Meta': {'object_name': 'Building', 'unique_together': "(('address_1', 'address_2', 'city', 'postcode', 'country'),)"},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'FI'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'num_floors': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tickets.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'action': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'amenity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['amenities.Amenity']"}),
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['buildings.Apartment']"}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'handler': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'handled_tickets'", 'null': 'True', 'to': "orm['accounts.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'new'", 'no_check_for_status': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['tickets']