from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import django.dispatch
import datetime
#from libs.models.fields import ListField

class Tag(models.Model):
    name                = models.CharField(max_length=255, unique=True)
    author              = models.ForeignKey(User, null=True, blank=True, related_name='created_tags')
    deleted             = models.BooleanField(default=False)
    deleted_at          = models.DateTimeField(null=True, blank=True)
    deleted_by          = models.ForeignKey(User, null=True, blank=True, related_name='deleted_tags')

    # Denormalised data
    used_count          = models.PositiveIntegerField(default=0)
    
    # TODO: We need to figure this out
    #objects = TagManager()

    class Meta:
        db_table = u'tag'
        ordering = ('-used_count', 'name')
    def __unicode__(self):
        return self.name

class Image(models.Model):
    content_type        = models.ForeignKey(ContentType)
    object_id           = models.PositiveIntegerField()
    content_object      = generic.GenericForeignKey('content_type', 'object_id')
    local_image_src     = models.CharField(max_length=1024, blank=True)
    remote_image_src    = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = u'image'

class Comment(models.Model):
    content_type        = models.ForeignKey(ContentType)
    object_id           = models.PositiveIntegerField()
    content_object      = generic.GenericForeignKey('content_type', 'object_id')
    content             = models.CharField(max_length=1024)
    images              = generic.GenericRelation(Image)
    author              = models.ForeignKey(User, related_name='comments')

    # status
    added_at            = models.DateTimeField(default=datetime.datetime.now)
    deleted             = models.BooleanField(default=False)
    deleted_at          = models.DateTimeField(null=True, blank=True)
    deleted_by          = models.ForeignKey(User, null=True, blank=True, related_name='deleted_comments')

    # user preference 
    liked_by            = models.ManyToManyField(User, null=True, blank=True, related_name='liked_comments')
    like_count          = models.PositiveIntegerField(default=0)
    comments            = generic.GenericRelation('self')
    comment_count       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-added_at',)
        db_table = u'comment'

    def __unicode__(self):
        return self.content

class Post(models.Model):
    title               = models.CharField(max_length=300, unique=True)
    author              = models.ForeignKey(User, related_name='posts')
    post_source         = models.CharField(max_length=1024)
    content             = models.CharField(max_length=1024)
    images              = generic.GenericRelation(Image)
    tags                = models.ManyToManyField(Tag, null=True, blank=True, related_name='tagged_posts')

    # status
    added_at            = models.DateTimeField(default=datetime.datetime.now)
    deleted             = models.BooleanField(default=False)
    deleted_at          = models.DateTimeField(null=True, blank=True)
    deleted_by          = models.ForeignKey(User, null=True, blank=True, related_name='deleted_posts')

    # user preference 
    liked_by            = models.ManyToManyField(User, null=True, blank=True, related_name='liked_posts')
    like_count          = models.PositiveIntegerField(default=0)
    comments            = generic.GenericRelation(Comment)
    comment_count       = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.content
    class Meta:
        db_table = u'post'

# custom signal
user_logged_in = django.dispatch.Signal(providing_args=["session"])
