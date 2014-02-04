# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ErrorGroup.parent'
        db.alter_column(u'linted_errorgroup', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.ErrorGroup'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ErrorGroup.parent'
        raise RuntimeError("Cannot reverse this migration. 'ErrorGroup.parent' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'ErrorGroup.parent'
        db.alter_column(u'linted_errorgroup', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.ErrorGroup']))

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
        u'linted.errorgroup': {
            'Meta': {'object_name': 'ErrorGroup'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ErrorGroup']", 'null': 'True'})
        },
        u'linted.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'linted.linter': {
            'Meta': {'object_name': 'Linter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'linted.repository': {
            'Meta': {'object_name': 'Repository'},
            'clone_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'0aaebdd7-419e-4ee1-af8e-8a4ae442fe56'", 'unique': 'True', 'max_length': '40'})
        },
        u'linted.repositorykey': {
            'Meta': {'object_name': 'RepositoryKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private_key': ('django.db.models.fields.TextField', [], {}),
            'public_key': ('django.db.models.fields.TextField', [], {}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"})
        },
        u'linted.repositorylinter': {
            'Meta': {'object_name': 'RepositoryLinter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Linter']"}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"}),
            'settings': ('django.db.models.fields.TextField', [], {})
        },
        u'linted.repositoryscan': {
            'Meta': {'object_name': 'RepositoryScan'},
            'completed_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"})
        },
        u'linted.repositoryuser': {
            'Meta': {'object_name': 'RepositoryUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'linted.scanerror': {
            'Meta': {'object_name': 'ScanError'},
            'end_line': ('django.db.models.fields.IntegerField', [], {}),
            'error_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ErrorGroup']"}),
            'file': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Linter']"}),
            'previous_error': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ScanError']"}),
            'scan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.RepositoryScan']"}),
            'snippet': ('django.db.models.fields.TextField', [], {}),
            'start_line': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['linted']