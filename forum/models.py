from django.db import models
import django.dispatch
from libs.models.fields import ListField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60, unique=True)
    content = models.CharField(max_length=1024)

    # like pool
    likedBy = ListField(null=True)
    like_count = models.IntegerField(default=0)
    # for post categorization
    tags = ListField(null=True)

    def __unicode__(self):
        return self.content

# custom signal
user_logged_in = django.dispatch.Signal(providing_args=["session"])

