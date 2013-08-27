from django.db import models
import django.dispatch
from django.contrib.auth.models import User
#from libs.models.fields import ListField

# Create your models here.
class Post(models.Model):
    title       = models.CharField(max_length=300, unique=True)
    author      = models.ForeignKey(User, related_name='posts')
    post_source = models.CharField(max_length=1024)
    # TODO: how to store image
    #img_source
    content     = models.CharField(max_length=1024)
    tags        = models.ManyToManyField(Tag, related_name='posts')

    # status
    added_at    = models.DateTimeField(default=datetime.datetime.now)
    deleted     = models.BooleanField(default=False)
    deleted_at  = models.DateTimeField(null=True, blank=True)
    deleted_by  = models.ForeignKey(User, null=True, blank=True, related_name='deleted_tags')

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
    added_at       = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('-added_at',)
        db_table = u'comment'
    def __unicode__(self):
        return self.comment

# custom signal
user_logged_in = django.dispatch.Signal(providing_args=["session"])

