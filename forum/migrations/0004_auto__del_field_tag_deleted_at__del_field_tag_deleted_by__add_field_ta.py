# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Tag.deleted_at'
        db.delete_column(u'tag', 'deleted_at')

        # Deleting field 'Tag.deleted_by'
        db.delete_column(u'tag', 'deleted_by_id')

        # Adding field 'Tag.added_at'
        db.add_column(u'tag', 'added_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 8, 9, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Tag.updated_at'
        db.add_column(u'tag', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 9, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Post.post_source_name'
        db.delete_column(u'post', 'post_source_name')

        # Deleting field 'Post.post_source_url'
        db.delete_column(u'post', 'post_source_url')

        # Deleting field 'Post.deleted_by'
        db.delete_column(u'post', 'deleted_by_id')

        # Deleting field 'Post.deleted_at'
        db.delete_column(u'post', 'deleted_at')

        # Adding field 'Post.updated_at'
        db.add_column(u'post', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 9, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Post.added_at'
        db.alter_column(u'post', 'added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Deleting field 'Comment.deleted_at'
        db.delete_column(u'comment', 'deleted_at')

        # Deleting field 'Comment.deleted_by'
        db.delete_column(u'comment', 'deleted_by_id')

        # Adding field 'Comment.updated_at'
        db.add_column(u'comment', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 9, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Comment.added_at'
        db.alter_column(u'comment', 'added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Adding field 'Tag.deleted_at'
        db.add_column(u'tag', 'deleted_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tag.deleted_by'
        db.add_column(u'tag', 'deleted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='deleted_tags', null=True, to=orm['auth.User'], blank=True),
                      keep_default=False)

        # Deleting field 'Tag.added_at'
        db.delete_column(u'tag', 'added_at')

        # Deleting field 'Tag.updated_at'
        db.delete_column(u'tag', 'updated_at')

        # Adding field 'Post.post_source_name'
        db.add_column(u'post', 'post_source_name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 8, 9, 0, 0), max_length=64),
                      keep_default=False)

        # Adding field 'Post.post_source_url'
        db.add_column(u'post', 'post_source_url',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 8, 9, 0, 0), max_length=1024),
                      keep_default=False)

        # Adding field 'Post.deleted_by'
        db.add_column(u'post', 'deleted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='deleted_posts', null=True, to=orm['auth.User'], blank=True),
                      keep_default=False)

        # Adding field 'Post.deleted_at'
        db.add_column(u'post', 'deleted_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Post.updated_at'
        db.delete_column(u'post', 'updated_at')


        # Changing field 'Post.added_at'
        db.alter_column(u'post', 'added_at', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'Comment.deleted_at'
        db.add_column(u'comment', 'deleted_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Comment.deleted_by'
        db.add_column(u'comment', 'deleted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='deleted_comments', null=True, to=orm['auth.User'], blank=True),
                      keep_default=False)

        # Deleting field 'Comment.updated_at'
        db.delete_column(u'comment', 'updated_at')


        # Changing field 'Comment.added_at'
        db.alter_column(u'comment', 'added_at', self.gf('django.db.models.fields.DateTimeField')())

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
        u'forum.comment': {
            'Meta': {'ordering': "('-added_at',)", 'object_name': 'Comment', 'db_table': "u'comment'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['auth.User']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'liked_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'forum.image': {
            'Meta': {'object_name': 'Image', 'db_table': "u'image'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'forum.post': {
            'Meta': {'object_name': 'Post', 'db_table': "u'post'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['auth.User']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '8192'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'liked_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tagged_posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['forum.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'forum.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "u'resource'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'resource_src': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        u'forum.tag': {
            'Meta': {'ordering': "('-used_count', 'name')", 'object_name': 'Tag', 'db_table': "u'tag'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_tags'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['forum']