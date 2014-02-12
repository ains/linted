# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Repository'
        db.create_table(u'linted_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('uuid',
             self.gf('django.db.models.fields.CharField')(default='5c29113b-faef-4026-b8f6-c7880516e9ef', unique=True,
                                                          max_length=40)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clone_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'linted', ['Repository'])

        # Adding model 'RepositoryUser'
        db.create_table(u'linted_repositoryuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Repository'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'linted', ['RepositoryUser'])

        # Adding model 'RepositoryKey'
        db.create_table(u'linted_repositorykey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Repository'])),
            ('private_key', self.gf('django.db.models.fields.TextField')()),
            ('public_key', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'linted', ['RepositoryKey'])

        # Adding model 'Language'
        db.create_table(u'linted_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'linted', ['Language'])

        # Adding model 'Scanner'
        db.create_table(u'linted_scanner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Language'])),
        ))
        db.send_create_signal(u'linted', ['Scanner'])

        # Adding model 'RepositoryScanner'
        db.create_table(u'linted_repositoryscanner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Repository'])),
            ('scanner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Scanner'])),
            ('settings', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'linted', ['RepositoryScanner'])

        # Adding model 'RepositoryScan'
        db.create_table(u'linted_repositoryscan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Repository'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('completed_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'linted', ['RepositoryScan'])

        # Adding model 'ErrorGroup'
        db.create_table(u'linted_errorgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.ErrorGroup'], null=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'linted', ['ErrorGroup'])

        # Adding model 'ScanViolation'
        db.create_table(u'linted_scanviolation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.RepositoryScan'])),
            ('scanner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.Scanner'])),
            ('previous_error',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.ScanViolation'], null=True)),
            ('error_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linted.ErrorGroup'])),
            ('file', self.gf('django.db.models.fields.TextField')(max_length=256)),
            ('start_line', self.gf('django.db.models.fields.IntegerField')()),
            ('end_line', self.gf('django.db.models.fields.IntegerField')()),
            ('snippet', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'linted', ['ScanViolation'])


    def backwards(self, orm):
        # Deleting model 'Repository'
        db.delete_table(u'linted_repository')

        # Deleting model 'RepositoryUser'
        db.delete_table(u'linted_repositoryuser')

        # Deleting model 'RepositoryKey'
        db.delete_table(u'linted_repositorykey')

        # Deleting model 'Language'
        db.delete_table(u'linted_language')

        # Deleting model 'Scanner'
        db.delete_table(u'linted_scanner')

        # Deleting model 'RepositoryScanner'
        db.delete_table(u'linted_repositoryscanner')

        # Deleting model 'RepositoryScan'
        db.delete_table(u'linted_repositoryscan')

        # Deleting model 'ErrorGroup'
        db.delete_table(u'linted_errorgroup')

        # Deleting model 'ScanViolation'
        db.delete_table(u'linted_scanviolation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
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
            'parent': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ErrorGroup']", 'null': 'True'})
        },
        u'linted.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'uuid': ('django.db.models.fields.CharField', [],
                     {'default': "'c6c1920f-899f-4605-87d8-213688b117f9'", 'unique': 'True', 'max_length': '40'})
        },
        u'linted.repositorykey': {
            'Meta': {'object_name': 'RepositoryKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private_key': ('django.db.models.fields.TextField', [], {}),
            'public_key': ('django.db.models.fields.TextField', [], {}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"})
        },
        u'linted.repositoryscan': {
            'Meta': {'object_name': 'RepositoryScan'},
            'completed_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"})
        },
        u'linted.repositoryscanner': {
            'Meta': {'object_name': 'RepositoryScanner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"}),
            'scanner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Scanner']"}),
            'settings': ('django.db.models.fields.TextField', [], {})
        },
        u'linted.repositoryuser': {
            'Meta': {'object_name': 'RepositoryUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Repository']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'linted.scanner': {
            'Meta': {'object_name': 'Scanner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        u'linted.scanviolation': {
            'Meta': {'object_name': 'ScanViolation'},
            'end_line': ('django.db.models.fields.IntegerField', [], {}),
            'error_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ErrorGroup']"}),
            'file': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_error': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.ScanViolation']", 'null': 'True'}),
            'scan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.RepositoryScan']"}),
            'scanner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linted.Scanner']"}),
            'snippet': ('django.db.models.fields.TextField', [], {}),
            'start_line': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['linted']