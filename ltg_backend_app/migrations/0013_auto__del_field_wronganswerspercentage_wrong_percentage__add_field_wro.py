# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WrongAnswersPercentage.wrong_percentage'
        db.delete_column(u'ltg_backend_app_wronganswerspercentage', 'wrong_percentage')

        # Adding field 'WrongAnswersPercentage.percentage_wrong'
        db.add_column(u'ltg_backend_app_wronganswerspercentage', 'percentage_wrong',
                      self.gf('django.db.models.fields.DecimalField')(default=10.0, max_digits=5, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'WrongAnswersPercentage.wrong_percentage'
        db.add_column(u'ltg_backend_app_wronganswerspercentage', 'wrong_percentage',
                      self.gf('django.db.models.fields.DecimalField')(default=10.0, max_digits=5, decimal_places=2),
                      keep_default=False)

        # Deleting field 'WrongAnswersPercentage.percentage_wrong'
        db.delete_column(u'ltg_backend_app_wronganswerspercentage', 'percentage_wrong')


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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.concept': {
            'Meta': {'object_name': 'Concept'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.UserProfile']", 'through': u"orm['ltg_backend_app.Attempt']", 'symmetrical': 'False'}),
            'concepts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'symmetrical': 'False'})
        },
        u'ltg_backend_app.questionstatistics': {
            'Meta': {'unique_together': "(('question', 'attempt'),)", 'object_name': 'QuestionStatistics', 'index_together': "[['question', 'attempt']]"},
            'attempt': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_time': ('timedelta.fields.TimedeltaField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'percentage_right': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'std_time': ('timedelta.fields.TimedeltaField', [], {})
        },
        u'ltg_backend_app.scoretable': {
            'Meta': {'object_name': 'ScoreTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.section': {
            'Meta': {'object_name': 'Section'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.userconceptscore': {
            'Meta': {'object_name': 'UserConceptScore'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.usersectionscore': {
            'Meta': {'object_name': 'UserSectionScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.UserProfile']"})
        },
        u'ltg_backend_app.wronganswerspercentage': {
            'Meta': {'object_name': 'WrongAnswersPercentage'},
            'answer': ('django.db.models.fields.SmallIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 13, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'percentage_wrong': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'question_statistic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.QuestionStatistics']"})
        }
    }

    complete_apps = ['ltg_backend_app']