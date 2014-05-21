# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Concept'
        db.create_table(u'ltg_backend_app_concept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['Concept'])

        # Adding model 'Section'
        db.create_table(u'ltg_backend_app_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['Section'])

        # Adding model 'LtgUser'
        db.create_table(u'ltg_backend_app_ltguser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(default='d0aab24230204fd4b35134f1471d74', unique=True, max_length=30)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'ltg_backend_app', ['LtgUser'])

        # Adding M2M table for field groups on 'LtgUser'
        m2m_table_name = db.shorten_name(u'ltg_backend_app_ltguser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ltguser', models.ForeignKey(orm[u'ltg_backend_app.ltguser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ltguser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'LtgUser'
        m2m_table_name = db.shorten_name(u'ltg_backend_app_ltguser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ltguser', models.ForeignKey(orm[u'ltg_backend_app.ltguser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ltguser_id', 'permission_id'])

        # Adding model 'UserScore'
        db.create_table(u'ltg_backend_app_userscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.LtgUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserScore'])

        # Adding model 'UserConceptScore'
        db.create_table(u'ltg_backend_app_userconceptscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.LtgUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Concept'])),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserConceptScore'])

        # Adding model 'UserSectionScore'
        db.create_table(u'ltg_backend_app_usersectionscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.LtgUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Section'])),
        ))
        db.send_create_signal(u'ltg_backend_app', ['UserSectionScore'])

        # Adding model 'Question'
        db.create_table(u'ltg_backend_app_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('answer', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['Question'])

        # Adding M2M table for field concepts on 'Question'
        m2m_table_name = db.shorten_name(u'ltg_backend_app_question_concepts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'ltg_backend_app.question'], null=False)),
            ('concept', models.ForeignKey(orm[u'ltg_backend_app.concept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'concept_id'])

        # Adding M2M table for field sections on 'Question'
        m2m_table_name = db.shorten_name(u'ltg_backend_app_question_sections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'ltg_backend_app.question'], null=False)),
            ('section', models.ForeignKey(orm[u'ltg_backend_app.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'section_id'])

        # Adding model 'Attempt'
        db.create_table(u'ltg_backend_app_attempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.LtgUser'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Question'])),
            ('attempt', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('answer', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('duration', self.gf('timedelta.fields.TimedeltaField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['Attempt'])

        # Adding unique constraint on 'Attempt', fields ['user', 'question', 'attempt']
        db.create_unique(u'ltg_backend_app_attempt', ['user_id', 'question_id', 'attempt'])

        # Adding index on 'Attempt', fields ['question', 'attempt']
        db.create_index(u'ltg_backend_app_attempt', ['question_id', 'attempt'])

        # Adding model 'ScoreTable'
        db.create_table(u'ltg_backend_app_scoretable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentile', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['ScoreTable'])

        # Adding model 'QuestionStatistics'
        db.create_table(u'ltg_backend_app_questionstatistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Question'])),
            ('attempt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('attempts_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mean_time', self.gf('timedelta.fields.TimedeltaField')()),
            ('std_time', self.gf('timedelta.fields.TimedeltaField')()),
            ('percentage_right', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['QuestionStatistics'])

        # Adding unique constraint on 'QuestionStatistics', fields ['question', 'attempt']
        db.create_unique(u'ltg_backend_app_questionstatistics', ['question_id', 'attempt'])

        # Adding index on 'QuestionStatistics', fields ['question', 'attempt']
        db.create_index(u'ltg_backend_app_questionstatistics', ['question_id', 'attempt'])

        # Adding model 'WrongAnswersPercentage'
        db.create_table(u'ltg_backend_app_wronganswerspercentage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('percentage_wrong', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('question_statistics', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.QuestionStatistics'])),
        ))
        db.send_create_signal(u'ltg_backend_app', ['WrongAnswersPercentage'])

        # Adding model 'ConceptStatistics'
        db.create_table(u'ltg_backend_app_conceptstatistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Concept'])),
            ('mean_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('std_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['ConceptStatistics'])

        # Adding model 'SectionStatistics'
        db.create_table(u'ltg_backend_app_sectionstatistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('modified_data', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0), auto_now=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ltg_backend_app.Section'])),
            ('mean_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('std_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ltg_backend_app', ['SectionStatistics'])


    def backwards(self, orm):
        # Removing index on 'QuestionStatistics', fields ['question', 'attempt']
        db.delete_index(u'ltg_backend_app_questionstatistics', ['question_id', 'attempt'])

        # Removing unique constraint on 'QuestionStatistics', fields ['question', 'attempt']
        db.delete_unique(u'ltg_backend_app_questionstatistics', ['question_id', 'attempt'])

        # Removing index on 'Attempt', fields ['question', 'attempt']
        db.delete_index(u'ltg_backend_app_attempt', ['question_id', 'attempt'])

        # Removing unique constraint on 'Attempt', fields ['user', 'question', 'attempt']
        db.delete_unique(u'ltg_backend_app_attempt', ['user_id', 'question_id', 'attempt'])

        # Deleting model 'Concept'
        db.delete_table(u'ltg_backend_app_concept')

        # Deleting model 'Section'
        db.delete_table(u'ltg_backend_app_section')

        # Deleting model 'LtgUser'
        db.delete_table(u'ltg_backend_app_ltguser')

        # Removing M2M table for field groups on 'LtgUser'
        db.delete_table(db.shorten_name(u'ltg_backend_app_ltguser_groups'))

        # Removing M2M table for field user_permissions on 'LtgUser'
        db.delete_table(db.shorten_name(u'ltg_backend_app_ltguser_user_permissions'))

        # Deleting model 'UserScore'
        db.delete_table(u'ltg_backend_app_userscore')

        # Deleting model 'UserConceptScore'
        db.delete_table(u'ltg_backend_app_userconceptscore')

        # Deleting model 'UserSectionScore'
        db.delete_table(u'ltg_backend_app_usersectionscore')

        # Deleting model 'Question'
        db.delete_table(u'ltg_backend_app_question')

        # Removing M2M table for field concepts on 'Question'
        db.delete_table(db.shorten_name(u'ltg_backend_app_question_concepts'))

        # Removing M2M table for field sections on 'Question'
        db.delete_table(db.shorten_name(u'ltg_backend_app_question_sections'))

        # Deleting model 'Attempt'
        db.delete_table(u'ltg_backend_app_attempt')

        # Deleting model 'ScoreTable'
        db.delete_table(u'ltg_backend_app_scoretable')

        # Deleting model 'QuestionStatistics'
        db.delete_table(u'ltg_backend_app_questionstatistics')

        # Deleting model 'WrongAnswersPercentage'
        db.delete_table(u'ltg_backend_app_wronganswerspercentage')

        # Deleting model 'ConceptStatistics'
        db.delete_table(u'ltg_backend_app_conceptstatistics')

        # Deleting model 'SectionStatistics'
        db.delete_table(u'ltg_backend_app_sectionstatistics')


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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.concept': {
            'Meta': {'object_name': 'Concept'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.conceptstatistics': {
            'Meta': {'object_name': 'ConceptStatistics'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'std_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.ltguser': {
            'Meta': {'object_name': 'LtgUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
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
            'username': ('django.db.models.fields.CharField', [], {'default': "'f827e28423634b39980dcae35649a1'", 'unique': 'True', 'max_length': '30'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'ltg_backend_app.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.LtgUser']", 'through': u"orm['ltg_backend_app.Attempt']", 'symmetrical': 'False'}),
            'concepts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Concept']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ltg_backend_app.Section']", 'symmetrical': 'False'})
        },
        u'ltg_backend_app.questionstatistics': {
            'Meta': {'unique_together': "(('question', 'attempt'),)", 'object_name': 'QuestionStatistics', 'index_together': "[['question', 'attempt']]"},
            'attempt': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'attempts_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_time': ('timedelta.fields.TimedeltaField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'ltg_backend_app.sectionstatistics': {
            'Meta': {'object_name': 'SectionStatistics'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'std_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ltg_backend_app.userconceptscore': {
            'Meta': {'object_name': 'UserConceptScore'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Concept']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.usersectionscore': {
            'Meta': {'object_name': 'UserSectionScore'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.Section']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.LtgUser']"})
        },
        u'ltg_backend_app.wronganswerspercentage': {
            'Meta': {'object_name': 'WrongAnswersPercentage'},
            'answer': ('django.db.models.fields.SmallIntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'percentage_wrong': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'question_statistics': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ltg_backend_app.QuestionStatistics']"})
        }
    }

    complete_apps = ['ltg_backend_app']