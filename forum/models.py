from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import django.dispatch
import datetime
#from libs.models.fields import ListField

class Tag(models.Model):
    name            = models.CharField(max_length=255, unique=True)
    author          = models.ForeignKey(User, related_name='created_tags')
    deleted         = models.BooleanField(default=False)
    deleted_at      = models.DateTimeField(null=True, blank=True)
    deleted_by      = models.ForeignKey(User, null=True, blank=True, related_name='deleted_tags')

    # Denormalised data
    used_count = models.PositiveIntegerField(default=0)
    
    # TODO: We need to figure this out
    #objects = TagManager()

    class Meta:
        db_table = u'tag'
        ordering = ('-used_count', 'name')
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    author         = models.ForeignKey(User, related_name='comments')
    content        = models.CharField(max_length=300)
    image_src      = models.CharField(max_length=300)

    # status
    added_at       = models.DateTimeField(default=datetime.datetime.now)
    deleted        = models.BooleanField(default=False)
    deleted_at     = models.DateTimeField(null=True, blank=True)
    deleted_by     = models.ForeignKey(User, null=True, blank=True, related_name='deleted_comments')

    # user preference 
    liked_by       = generic.GenericRelation(User)
    like_count     = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-added_at',)
        db_table = u'comment'
    def __unicode__(self):
        return self.comment

class Post(models.Model):
    title       = models.CharField(max_length=300, unique=True)
    author      = models.ForeignKey(User, related_name='posts')
    post_source = models.CharField(max_length=1024, null=True, blank=True)
    # TODO: how to store image
    content     = models.CharField(max_length=1024)
    image_src   = models.CharField(max_length=300, null=True, blank=True)
    tags        = models.ManyToManyField(Tag, null=True, blank=True, related_name='posts')

    # status
    added_at    = models.DateTimeField(default=datetime.datetime.now)
    deleted     = models.BooleanField(default=False)
    deleted_at  = models.DateTimeField(null=True, blank=True)
    deleted_by  = models.ForeignKey(User, null=True, blank=True, related_name='deleted_posts')

    # user preference 
    liked_by    = generic.GenericRelation(User)
    comments    = generic.GenericRelation(Comment)
    view_count  = models.PositiveIntegerField(default=0)
    like_count  = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.content
    class Meta:
        db_table = u'post'

# custom signal
user_logged_in = django.dispatch.Signal(providing_args=["session"])

