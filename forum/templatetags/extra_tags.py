import time
import datetime
import math
import re
import logging
from django import template
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def get_user_like_image(users, user):
    if user in users.all():
        return 'd'
    return ''
        
@register.filter
def is_liked_by(post, user):
    if user in post.liked_by.all():
        return True
    return False
