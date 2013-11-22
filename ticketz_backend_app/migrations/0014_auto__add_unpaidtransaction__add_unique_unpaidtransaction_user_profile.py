# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnpaidTransaction'
        db.create_table('ticketz_backend_app_unpaidtransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 22, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 22, 0, 0), auto_now=True, blank=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticketz_backend_app.UserProfile'])),
            ('deal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticketz_backend_app.Deal'])),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('hash', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('ticketz_backend_app', ['UnpaidTransaction'])

        # Adding unique constraint on 'UnpaidTransaction', fields ['user_profile', 'deal']
        db.create_unique('ticketz_backend_app_unpaidtransaction', ['user_profile_id', 'deal_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UnpaidTransaction', fields ['user_profile', 'deal']
        db.delete_unique('ticketz_backend_app_unpaidtransaction', ['user_profile_id', 'deal_id'])

        # Deleting model 'UnpaidTransaction'
        db.delete_table('ticketz_backend_app_unpaidtransaction')


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
            'business_number': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'web_service_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'ticketz_backend_app.category': {
            'Meta': {'object_name': 'Category'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.city': {
            'Meta': {'object_name': 'City'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['ticketz_backend_app.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.deal': {
            'Meta': {'object_name': 'Deal'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticketz_backend_app.Business']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.Category']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'discounted_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'num_total_places': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'original_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'})
        },
        'ticketz_backend_app.flatpage': {
            'Meta': {'object_name': 'FlatPage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'ticketz_backend_app.logger': {
            'Meta': {'object_name': 'Logger'},
            'content': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'get': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        'ticketz_backend_app.region': {
            'Meta': {'object_name': 'Region'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ticketz_backend_app.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticketz_backend_app.Deal']"}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'paymill_transaction_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticketz_backend_app.UserProfile']"})
        },
        'ticketz_backend_app.unpaidtransaction': {
            'Meta': {'unique_together': "(('user_profile', 'deal'),)", 'object_name': 'UnpaidTransaction'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticketz_backend_app.Deal']"}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticketz_backend_app.UserProfile']"})
        },
        'ticketz_backend_app.userprefrence': {
            'Meta': {'object_name': 'UserPrefrence'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ticketz_backend_app.Region']", 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefrences'", 'unique': 'True', 'to': "orm['ticketz_backend_app.UserProfile']"})
        },
        'ticketz_backend_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'user_profile'", 'null': 'True', 'blank': 'True', 'to': "orm['ticketz_backend_app.Business']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'paymill_client_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'paymill_payment_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ticketz_backend_app']