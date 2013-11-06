# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'nerdeez_server_app_course')

        # Deleting model 'University'
        db.delete_table(u'nerdeez_server_app_university')

        # Adding model 'SchoolGroup'
        db.create_table(u'nerdeez_server_app_schoolgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='university', null=True, blank=True, to=orm['nerdeez_server_app.SchoolGroup'])),
            ('school_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['SchoolGroup'])


    def backwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'nerdeez_server_app_course', (
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(related_name='university', null=True, to=orm['nerdeez_server_app.University'], blank=True)),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 17, 0, 0), auto_now=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 17, 0, 0))),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['Course'])

        # Adding model 'University'
        db.create_table(u'nerdeez_server_app_university', (
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 17, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 17, 0, 0))),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['University'])

        # Deleting model 'SchoolGroup'
        db.delete_table(u'nerdeez_server_app_schoolgroup')


    models = {
        u'nerdeez_server_app.flatpage': {
            'Meta': {'object_name': 'Flatpage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 7, 0, 0)'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'nerdeez_server_app.schoolgroup': {
            'Meta': {'object_name': 'SchoolGroup'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 7, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'university'", 'null': 'True', 'blank': 'True', 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'school_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['nerdeez_server_app']