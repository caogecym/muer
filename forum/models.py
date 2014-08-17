from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from forum.managers import TagManager
import django.dispatch

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, null=True, blank=True, related_name='created_tags')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # Denormalised data
    used_count = models.PositiveIntegerField(default=0)
    objects = TagManager()

    class Meta:
        db_table = u'tag'
        ordering = ('-used_count', 'name')

    def __unicode__(self):
        return self.name

class Image(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    image_src = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = u'image'

class Resource(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    resource_src = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = u'resource'

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    content = models.CharField(max_length=1024)
    images = generic.GenericRelation(Image)
    resources = generic.GenericRelation(Resource)
    author = models.ForeignKey(User, related_name='comments')

    # status
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # user preference
    liked_by = models.ManyToManyField(User, null=True, blank=True, related_name='liked_comments')
    like_count = models.PositiveIntegerField(default=0)
    comments = generic.GenericRelation('self')
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-added_at',)
        db_table = u'comment'

    def __unicode__(self):
        return self.content

class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    author = models.ForeignKey(User, related_name='posts')
    content = models.CharField(max_length=8192)  # in html
    images = generic.GenericRelation(Image)

    # store useful info other than image, like seed, attachment
    resources = generic.GenericRelation(Resource)
    tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='tagged_posts')
    tagnames = models.CharField(max_length=255)

    # status
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # user preference
    liked_by = models.ManyToManyField(User, null=True, blank=True, related_name='liked_posts')
    like_count = models.PositiveIntegerField(default=0)
    comments = generic.GenericRelation(Comment)
    comment_count = models.PositiveIntegerField(default=0)

    def save(self, **kwargs):
        """
        Overridden to manually manage addition of tags when the object
        is first saved.

        This is required as we're using ``tagnames`` as the sole means of
        adding and editing tags.
        """
        initial_addition = (self.id is None)
        super(Post, self).save(**kwargs)
        if initial_addition:
            tags = Tag.objects.get_or_create_multiple(self.tagname_list(),
                                                      self.author)
            self.tags.add(*tags)
            # Tag.objects.update_use_counts(tags)

    def tagname_list(self):
        """Creates a list of Tag names from the ``tagnames`` attribute."""
        return [name for name in self.tagnames.split(u' ')]

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = u'post'

# custom signal
user_logged_in = django.dispatch.Signal(providing_args=["session"])
