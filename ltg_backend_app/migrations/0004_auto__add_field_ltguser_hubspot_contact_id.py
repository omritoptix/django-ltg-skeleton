# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LtgUser.hubspot_contact_id'
        db.add_column(u'ltg_backend_app_ltguser', 'hubspot_contact_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LtgUser.hubspot_contact_id'
        db.delete_column(u'ltg_backend_app_ltguser', 'hubspot_contact_id')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ltg_backend_app.attempt': {
            'Meta': {'unique_together': "(('user', 'question', 'attempt'),)", 'object_name': 'Attempt', 'index_together': "[['question', 'attempt']]"},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.concept': {
            'Meta': {'object_name': 'Concept'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.conceptstatistics': {
            'Meta': {'object_name': 'ConceptStatistics'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'std_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.ltguser': {
            'Meta': {'object_name': 'LtgUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'device_last_logged_in': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'hubspot_contact_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'num_of_sessions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'platform_last_logged_in': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_GMAT_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'previous_GMAT_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'target_GMAT_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'test_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tutor_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'65d47265e81c464bb725e3865f553e'", 'max_length': '30'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'ltg_backend_app.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.LtgUser']", 'through': u"orm['ltg_backend_app.Attempt']", 'symmetrical': 'False'}),
            'concepts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'symmetrical': 'False'})
        },
        u'ltg_backend_app.questionstatistics': {
            'Meta': {'unique_together': "(('question', 'attempt'),)", 'object_name': 'QuestionStatistics', 'index_together': "[['question', 'attempt']]"},
            'attempt': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_time': ('timedelta.fields.TimedeltaField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.sectionstatistics': {
            'Meta': {'object_name': 'SectionStatistics'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'std_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.userconceptscore': {
            'Meta': {'object_name': 'UserConceptScore'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.usersectionscore': {
            'Meta': {'object_name': 'UserSectionScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.wronganswerspercentage': {
            'Meta': {'object_name': 'WrongAnswersPercentage'},
            'answer': ('django.db.models.fields.SmallIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'percentage_wrong': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'question_statistics': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.QuestionStatistics']"})
        }
    }

    complete_apps = ['ltg_backend_app']