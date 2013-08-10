from django.db import models
from libs.models.fields import ListField

# Create your models here.
class UserAccount(models.Model):
    # TODO: how user id can be and joke id can be shared between each other 
    user_name = models.CharField(max_length=60)
    user_pw = models.CharField(max_length=60)
    user_email = models.CharField(max_length=60)

    # like pool
    liked = ListField(null=True)
    # user preference
    tags = ListField(null=True)

    def __unicode__(self):
        return self.user_name

