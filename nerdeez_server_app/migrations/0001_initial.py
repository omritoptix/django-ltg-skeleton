# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'University'
        db.create_table(u'nerdeez_server_app_university', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['University'])

        # Adding model 'Faculty'
        db.create_table(u'nerdeez_server_app_faculty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='university', null=True, to=orm['nerdeez_server_app.University'])),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['Faculty'])

        # Adding model 'Course'
        db.create_table(u'nerdeez_server_app_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 30, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='faculty', null=True, to=orm['nerdeez_server_app.Faculty'])),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['Course'])


    def backwards(self, orm):
        # Deleting model 'University'
        db.delete_table(u'nerdeez_server_app_university')

        # Deleting model 'Faculty'
        db.delete_table(u'nerdeez_server_app_faculty')

        # Deleting model 'Course'
        db.delete_table(u'nerdeez_server_app_course')


    models = {
        u'nerdeez_server_app.course': {
            'Meta': {'object_name': 'Course'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faculty'", 'null': 'True', 'to': u"orm['nerdeez_server_app.Faculty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'university'", 'null': 'True', 'to': u"orm['nerdeez_server_app.University']"})
        },
        u'nerdeez_server_app.university': {
            'Meta': {'object_name': 'University'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['nerdeez_server_app']