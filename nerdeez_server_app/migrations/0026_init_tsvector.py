'''
this is my own reciepe to iterate on the database and create tsvector in the school group

Created October 16th, 2013
@author: Yariv Katz
@version: 1.0
@copyright: Nerdeez Ltd.
'''

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        #this will iterate on all the records and set the search vector
        db.execute(
                   """
                   CREATE OR REPLACE FUNCTION create_record_vector(record_id int) RETURNS text AS
                    $$
                        DECLARE
                            sVector VARCHAR;
                            tTitle VARCHAR;
                            tDescription VARCHAR;
                            iParent_id INTEGER;
                        BEGIN
                            tTitle:=(SELECT title from nerdeez_server_app_schoolgroup where id=record_id);
                            tDescription:=(SELECT description from nerdeez_server_app_schoolgroup where id=record_id);
                            iParent_id:=(SELECT parent_id from nerdeez_server_app_schoolgroup where id=record_id);
                            IF iParent_id IS NULL THEN 
                                RETURN tTitle || ' ' || tDescription;
                            ELSE 
                                sVector:=create_record_vector(iParent_id) || ' ' || tTitle || ' ' || tDescription;
                                RETURN sVector;
                            END IF;
                            
                        END;
                    $$ LANGUAGE plpgsql;
                    
                    CREATE OR REPLACE FUNCTION create_tsvectors() RETURNS VOID
                    AS $$
                        DECLARE
                            r nerdeez_server_app_schoolgroup%%rowtype;
                        BEGIN
                            FOR r IN SELECT * FROM nerdeez_server_app_schoolgroup
                            LOOP
                                UPDATE nerdeez_server_app_schoolgroup SET search_index=to_tsvector(create_record_vector(r.id)) WHERE id=r.id;
                            END LOOP;
                        END;
                    $$ LANGUAGE plpgsql;
                    
                    SELECT create_tsvectors();
                   """
                   )
        
        #trigger on update or insert update the tsvector and also the sons tsvector
        db.execute(
                   """
                   CREATE OR REPLACE FUNCTION tsvector_schoolgroup_update_trigger_before() RETURNS TRIGGER AS $$
                    DECLARE
                        sVector VARCHAR;
                        r nerdeez_server_app_schoolgroup%%rowtype;
                        tTitle VARCHAR;
                        tDescription VARCHAR;
                        iParent_id INTEGER;
                    BEGIN
                        tTitle:=NEW.title;
                        tDescription:=NEW.description;
                        iParent_id:=NEW.parent_id;
                        IF iParent_id IS NULL THEN 
                            sVector:= tTitle || ' ' || tDescription;
                        ELSE 
                            sVector:=create_record_vector(iParent_id) || ' ' || tTitle || ' ' || tDescription;
                        END IF;
                        
                        --set the search vector
                        NEW.search_index:=to_tsvector(sVector);
                
                        return NEW;
                    END;
                $$ LANGUAGE plpgsql;
                
                CREATE OR REPLACE FUNCTION tsvector_schoolgroup_update_trigger_after() RETURNS TRIGGER AS $$
                    DECLARE
                        sVector VARCHAR;
                        r nerdeez_server_app_schoolgroup%%rowtype;
                        tTitle VARCHAR;
                        tDescription VARCHAR;
                        iParent_id INTEGER;
                    BEGIN
                
                        for r in select * from nerdeez_server_app_schoolgroup where parent_id=NEW.id
                        LOOP
                            update nerdeez_server_app_schoolgroup set search_index=to_tsvector(create_record_vector(r.id)) where id=r.id;
                        END LOOP;
                        return NEW;
                    END;
                $$ LANGUAGE plpgsql;
                
                CREATE TRIGGER tsvectorupdate_schoolgroup_before BEFORE INSERT OR UPDATE ON nerdeez_server_app_schoolgroup
                FOR EACH ROW EXECUTE PROCEDURE tsvector_schoolgroup_update_trigger_before();
                
                CREATE TRIGGER tsvectorupdate_schoolgroup_after AFTER INSERT OR UPDATE ON nerdeez_server_app_schoolgroup
                FOR EACH ROW EXECUTE PROCEDURE tsvector_schoolgroup_update_trigger_after();
                   """
                   )

    def backwards(self, orm):
        db.execute(
                   """
                       alter table nerdeez_server_app_schoolgroup DISABLE TRIGGER tsvectorupdate_schoolgroup_before ;
                       alter table nerdeez_server_app_schoolgroup DISABLE TRIGGER tsvectorupdate_schoolgroup_after ;
                       DROP FUNCTION tsvector_schoolgroup_update_trigger_before() CASCADE;
                       DROP FUNCTION tsvector_schoolgroup_update_trigger_after() CASCADE;
                       DROP FUNCTION create_tsvectors() CASCADE;
                       DROP FUNCTION create_record_vector() CASCADE;
                   """
                   )

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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_entered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'link_to_schoolgroup'", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolls'", 'to': u"orm['nerdeez_server_app.UserProfile']"})
        },
        u'nerdeez_server_app.file': {
            'Meta': {'ordering': "['title']", 'object_name': 'File'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'default': "'3.5'", 'max_digits': '3', 'decimal_places': '1'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'hw': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'files'", 'null': 'True', 'blank': 'True', 'to': u"orm['nerdeez_server_app.Hw']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.flatpage': {
            'Meta': {'object_name': 'Flatpage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'nerdeez_server_app.forgotpass': {
            'Meta': {'object_name': 'ForgotPass'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "'6lQC4TalRY12vXPoFePJXQXYH2c3akuHuEoTVhpbLjxfitvH6cKEsLLOLB2551rJ'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nerdeez_server_app.UserProfile']"})
        },
        u'nerdeez_server_app.hw': {
            'Meta': {'ordering': "['title']", 'object_name': 'Hw'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'default': "'3.5'", 'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hws'", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.schoolgroup': {
            'Meta': {'object_name': 'SchoolGroup'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'default': "'3.5'", 'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'university'", 'null': 'True', 'blank': 'True', 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'school_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'school_groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'through': u"orm['nerdeez_server_app.Enroll']", 'to': u"orm['nerdeez_server_app.SchoolGroup']"}),
            'twitter_oauth_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'twitter_oauth_token_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['nerdeez_server_app']