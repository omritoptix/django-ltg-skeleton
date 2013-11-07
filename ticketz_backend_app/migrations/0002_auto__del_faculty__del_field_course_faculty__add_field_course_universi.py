# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Faculty'
        db.delete_table(u'nerdeez_server_app_faculty')

        # Deleting field 'Course.faculty'
        db.delete_column(u'nerdeez_server_app_course', 'faculty_id')

        # Adding field 'Course.university'
        db.add_column(u'nerdeez_server_app_course', 'university',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='university', null=True, to=orm['nerdeez_server_app.University']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Faculty'
        db.create_table(u'nerdeez_server_app_faculty', (
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(related_name='university', null=True, to=orm['nerdeez_server_app.University'], blank=True)),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0), auto_now=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0))),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['Faculty'])

        # Adding field 'Course.faculty'
        db.add_column(u'nerdeez_server_app_course', 'faculty',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='faculty', null=True, to=orm['nerdeez_server_app.Faculty'], blank=True),
                      keep_default=False)

        # Deleting field 'Course.university'
        db.delete_column(u'nerdeez_server_app_course', 'university_id')


    models = {
        u'nerdeez_server_app.course': {
            'Meta': {'object_name': 'Course'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 12, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 12, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'university'", 'null': 'True', 'to': u"orm['nerdeez_server_app.University']"})
        },
        u'nerdeez_server_app.university': {
            'Meta': {'object_name': 'University'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 12, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 12, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['nerdeez_server_app']