from django.db import models
from libs.models.fields import ListField

# Create your models here.
class Joke(models.Model):
    title = models.CharField(max_length=60, unique=True)
    content = models.CharField(max_length=1024)

    # like pool
    likedBy = ListField(null=True)
    # for joke categorization
    tags = ListField(null=True)

    def __unicode__(self):
        return self.content
