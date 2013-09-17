# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created_tags', null=True, to=orm['auth.User'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deleted_tags', null=True, to=orm['auth.User'])),
            ('used_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'forum', ['Tag'])

        # Adding model 'Image'
        db.create_table(u'image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('local_image_src', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('remote_image_src', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'forum', ['Image'])

        # Adding model 'Resource'
        db.create_table(u'resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('local_resource_src', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('remote_resource_src', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'forum', ['Resource'])

        # Adding model 'Comment'
        db.create_table(u'comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['auth.User'])),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deleted_comments', null=True, to=orm['auth.User'])),
            ('like_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'forum', ['Comment'])

        # Adding M2M table for field liked_by on 'Comment'
        m2m_table_name = db.shorten_name(u'comment_liked_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'forum.comment'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'user_id'])

        # Adding model 'Post'
        db.create_table(u'post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['auth.User'])),
            ('post_source', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deleted_posts', null=True, to=orm['auth.User'])),
            ('like_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'forum', ['Post'])

        # Adding M2M table for field tags on 'Post'
        m2m_table_name = db.shorten_name(u'post_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'forum.post'], null=False)),
            ('tag', models.ForeignKey(orm[u'forum.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'tag_id'])

        # Adding M2M table for field liked_by on 'Post'
        m2m_table_name = db.shorten_name(u'post_liked_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'forum.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tag')

        # Deleting model 'Image'
        db.delete_table(u'image')

        # Deleting model 'Resource'
        db.delete_table(u'resource')

        # Deleting model 'Comment'
        db.delete_table(u'comment')

        # Removing M2M table for field liked_by on 'Comment'
        db.delete_table(db.shorten_name(u'comment_liked_by'))

        # Deleting model 'Post'
        db.delete_table(u'post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table(db.shorten_name(u'post_tags'))

        # Removing M2M table for field liked_by on 'Post'
        db.delete_table(db.shorten_name(u'post_liked_by'))


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
        u'forum.comment': {
            'Meta': {'ordering': "('-added_at',)", 'object_name': 'Comment', 'db_table': "u'comment'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['auth.User']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deleted_comments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'liked_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'forum.image': {
            'Meta': {'object_name': 'Image', 'db_table': "u'image'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_image_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remote_image_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        u'forum.post': {
            'Meta': {'object_name': 'Post', 'db_table': "u'post'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['auth.User']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deleted_posts'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'liked_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'post_source': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tagged_posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['forum.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'})
        },
        u'forum.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "u'resource'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_resource_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remote_resource_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        u'forum.tag': {
            'Meta': {'ordering': "('-used_count', 'name')", 'object_name': 'Tag', 'db_table': "u'tag'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_tags'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deleted_tags'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'used_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['forum']