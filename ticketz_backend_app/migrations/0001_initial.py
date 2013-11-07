# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('ticketz_backend_app_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('ticketz_backend_app', ['UserProfile'])

        # Adding model 'FlatPage'
        db.create_table('ticketz_backend_app_flatpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ticketz_backend_app', ['FlatPage'])

        # Adding model 'Region'
        db.create_table('ticketz_backend_app_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('ticketz_backend_app', ['Region'])

        # Adding model 'City'
        db.create_table('ticketz_backend_app_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['ticketz_backend_app.Region'])),
        ))
        db.send_create_signal('ticketz_backend_app', ['City'])

        # Adding model 'UserPrefrence'
        db.create_table('ticketz_backend_app_userprefrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prefrences', unique=True, to=orm['ticketz_backend_app.UserProfile'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ticketz_backend_app.City'], null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ticketz_backend_app.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('ticketz_backend_app', ['UserPrefrence'])

        # Adding model 'Category'
        db.create_table('ticketz_backend_app_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('ticketz_backend_app', ['Category'])

        # Adding model 'Business'
        db.create_table('ticketz_backend_app_business', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ticketz_backend_app.City'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('web_service_url', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True, blank=True)),
            ('adapter_class', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('paymill_private_key', self.gf('ticketz_backend_app.encryption.EncryptedCharField')(max_length=421)),
            ('adapter_object', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('ticketz_backend_app', ['Business'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('ticketz_backend_app_userprofile')

        # Deleting model 'FlatPage'
        db.delete_table('ticketz_backend_app_flatpage')

        # Deleting model 'Region'
        db.delete_table('ticketz_backend_app_region')

        # Deleting model 'City'
        db.delete_table('ticketz_backend_app_city')

        # Deleting model 'UserPrefrence'
        db.delete_table('ticketz_backend_app_userprefrence')

        # Deleting model 'Category'
        db.delete_table('ticketz_backend_app_category')

        # Deleting model 'Business'
        db.delete_table('ticketz_backend_app_business')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ticketz_backend_app.business': {
            'Meta': {'object_name': 'Business'},
            'adapter_class': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'adapter_object': ('picklefield.fields.PickledObjectField', [], {}),
            'address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'paymill_private_key': ('ticketz_backend_app.encryption.EncryptedCharField', [], {'max_length': '421'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'web_service_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'ticketz_backend_app.category': {
            'Meta': {'object_name': 'Category'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.city': {
            'Meta': {'object_name': 'City'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['ticketz_backend_app.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.flatpage': {
            'Meta': {'object_name': 'FlatPage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'ticketz_backend_app.region': {
            'Meta': {'object_name': 'Region'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.userprefrence': {
            'Meta': {'object_name': 'UserPrefrence'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.Region']", 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefrences'", 'unique': 'True', 'to': "orm['ticketz_backend_app.UserProfile']"})
        },
        'ticketz_backend_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ticketz_backend_app']