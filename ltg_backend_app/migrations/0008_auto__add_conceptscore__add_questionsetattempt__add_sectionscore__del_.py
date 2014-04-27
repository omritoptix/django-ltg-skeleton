# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Attempt', fields ['user', 'question', 'attempt']
        db.delete_unique(u'ltg_backend_app_attempt', ['user_id', 'question_id', 'attempt'])

        # Adding model 'ConceptScore'
        db.create_table(u'ltg_backend_app_conceptscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0), auto_now=True, blank=True)),
            ('question_set_attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.QuestionSetAttempt'])),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Concept'])),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['ConceptScore'])

        # Adding model 'QuestionSetAttempt'
        db.create_table(u'ltg_backend_app_questionsetattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['QuestionSetAttempt'])

        # Adding model 'SectionScore'
        db.create_table(u'ltg_backend_app_sectionscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 24, 0, 0), auto_now=True, blank=True)),
            ('question_set_attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.QuestionSetAttempt'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Section'])),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['SectionScore'])

        # Deleting field 'Attempt.user'
        db.delete_column(u'ltg_backend_app_attempt', 'user_id')

        # Adding field 'Attempt.user_profile'
        db.add_column(u'ltg_backend_app_attempt', 'user_profile',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['ltg_backend_app.UserProfile']),
                      keep_default=False)

        # Adding unique constraint on 'Attempt', fields ['user_profile', 'question', 'attempt']
        db.create_unique(u'ltg_backend_app_attempt', ['user_profile_id', 'question_id', 'attempt'])


    def backwards(self, orm):
        # Removing unique constraint on 'Attempt', fields ['user_profile', 'question', 'attempt']
        db.delete_unique(u'ltg_backend_app_attempt', ['user_profile_id', 'question_id', 'attempt'])

        # Deleting model 'ConceptScore'
        db.delete_table(u'ltg_backend_app_conceptscore')

        # Deleting model 'QuestionSetAttempt'
        db.delete_table(u'ltg_backend_app_questionsetattempt')

        # Deleting model 'SectionScore'
        db.delete_table(u'ltg_backend_app_sectionscore')

        # Adding field 'Attempt.user'
        db.add_column(u'ltg_backend_app_attempt', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Attempt.user_profile'
        db.delete_column(u'ltg_backend_app_attempt', 'user_profile_id')

        # Adding unique constraint on 'Attempt', fields ['user', 'question', 'attempt']
        db.create_unique(u'ltg_backend_app_attempt', ['user_id', 'question_id', 'attempt'])


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ltg_backend_app.attempt': {
            'Meta': {'unique_together': "(('user_profile', 'question', 'attempt'),)", 'object_name': 'Attempt'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.concept': {
            'Meta': {'object_name': 'Concept'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Question']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.conceptscore': {
            'Meta': {'object_name': 'ConceptScore'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question_set_attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.QuestionSetAttempt']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.UserProfile']", 'through': u"orm['ltg_backend_app.Attempt']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'ltg_backend_app.questionsetattempt': {
            'Meta': {'object_name': 'QuestionSetAttempt'},
            'concepts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'through': u"orm['ltg_backend_app.ConceptScore']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'through': u"orm['ltg_backend_app.SectionScore']", 'symmetrical': 'False'})
        },
        u'ltg_backend_app.scoretable': {
            'Meta': {'object_name': 'ScoreTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.section': {
            'Meta': {'object_name': 'Section'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Question']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.sectionscore': {
            'Meta': {'object_name': 'SectionScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question_set_attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.QuestionSetAttempt']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"})
        },
        u'ltg_backend_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['ltg_backend_app']