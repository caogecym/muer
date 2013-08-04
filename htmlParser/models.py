from django.db import models

# Create your models here.
class Joke(models.Model):
    title = models.CharField(max_length=60)
    content = models.CharField(max_length=1024)
    like = models.IntegerField()
    def __unicode__(self):
        return self.content
