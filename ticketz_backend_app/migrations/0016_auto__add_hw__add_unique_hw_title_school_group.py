# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hw'
        db.create_table(u'nerdeez_server_app_hw', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 6, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 6, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('grade', self.gf('django.db.models.fields.DecimalField')(default='3.5', max_digits=3, decimal_places=1)),
            ('school_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hws', to=orm['nerdeez_server_app.SchoolGroup'])),
        ))
        db.send_create_signal(u'nerdeez_server_app', ['Hw'])

        # Adding unique constraint on 'Hw', fields ['title', 'school_group']
        db.create_unique(u'nerdeez_server_app_hw', ['title', 'school_group_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Hw', fields ['title', 'school_group']
        db.delete_unique(u'nerdeez_server_app_hw', ['title', 'school_group_id'])

        # Deleting model 'Hw'
        db.delete_table(u'nerdeez_server_app_hw')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'nerdeez_server_app.enroll': {
            'Meta': {'ordering': "['-last_entered']", 'unique_together': "(('user', 'school_group'),)", 'object_name': 'Enroll'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_entered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'link_to_schoolgroup'", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolls'", 'to': u"orm['nerdeez_server_app.UserProfile']"})
        },
        u'nerdeez_server_app.flatpage': {
            'Meta': {'object_name': 'Flatpage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'nerdeez_server_app.forgotpass': {
            'Meta': {'object_name': 'ForgotPass'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "'XgCYOnUBvFCZ2jmHVeLM6OSWVaqjFBOs742zIRMZQmDIRPVjGVkU6KCKVmneZnhe'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nerdeez_server_app.UserProfile']"})
        },
        u'nerdeez_server_app.hw': {
            'Meta': {'ordering': "['title']", 'unique_together': "(('title', 'school_group'),)", 'object_name': 'Hw'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'default': "'3.5'", 'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hws'", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.schoolgroup': {
            'Meta': {'object_name': 'SchoolGroup'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'default': "'3.5'", 'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'university'", 'null': 'True', 'blank': 'True', 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'school_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'through': u"orm['nerdeez_server_app.Enroll']", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'twitter_oauth_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'twitter_oauth_token_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['nerdeez_server_app']