# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ConceptScore'
        db.delete_table(u'ltg_backend_app_conceptscore')

        # Deleting model 'QuestionSetAttempt'
        db.delete_table(u'ltg_backend_app_questionsetattempt')

        # Deleting model 'SectionScore'
        db.delete_table(u'ltg_backend_app_sectionscore')

        # Adding model 'UserScore'
        db.create_table(u'ltg_backend_app_userscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserScore'])

        # Adding model 'UserConceptScore'
        db.create_table(u'ltg_backend_app_userconceptscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Concept'])),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserConceptScore'])

        # Adding model 'UserSectionScore'
        db.create_table(u'ltg_backend_app_usersectionscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 7, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Section'])),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserSectionScore'])


    def backwards(self, orm):
        # Adding model 'ConceptScore'
        db.create_table(u'ltg_backend_app_conceptscore', (
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Concept'])),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0), auto_now=True, blank=True)),
            ('question_set_attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.QuestionSetAttempt'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0))),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['ConceptScore'])

        # Adding model 'QuestionSetAttempt'
        db.create_table(u'ltg_backend_app_questionsetattempt', (
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0), auto_now=True, blank=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.UserProfile'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0))),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['QuestionSetAttempt'])

        # Adding model 'SectionScore'
        db.create_table(u'ltg_backend_app_sectionscore', (
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0), auto_now=True, blank=True)),
            ('question_set_attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.QuestionSetAttempt'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Section'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 1, 0, 0))),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['SectionScore'])

        # Deleting model 'UserScore'
        db.delete_table(u'ltg_backend_app_userscore')

        # Deleting model 'UserConceptScore'
        db.delete_table(u'ltg_backend_app_userconceptscore')

        # Deleting model 'UserSectionScore'
        db.delete_table(u'ltg_backend_app_usersectionscore')


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
            'Meta': {'unique_together': "(('user_profile', 'question', 'attempt'),)", 'object_name': 'Attempt', 'index_together': "[['question', 'attempt']]"},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.concept': {
            'Meta': {'object_name': 'Concept'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.UserProfile']", 'through': u"orm['ltg_backend_app.Attempt']", 'symmetrical': 'False'}),
            'concepts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'symmetrical': 'False'})
        },
        u'ltg_backend_app.scoretable': {
            'Meta': {'object_name': 'ScoreTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.section': {
            'Meta': {'object_name': 'Section'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.userconceptscore': {
            'Meta': {'object_name': 'UserConceptScore'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'concept_scores': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'through': u"orm['ltg_backend_app.UserConceptScore']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'section_scores': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'through': u"orm['ltg_backend_app.UserSectionScore']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.usersectionscore': {
            'Meta': {'object_name': 'UserSectionScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 7, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        }
    }

    complete_apps = ['ltg_backend_app']