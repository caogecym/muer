from django import template

register = template.Library()

@register.simple_tag
def get_user_like_image(users, user):
    if user in users.all():
        return 'd'
    return ''

@register.filter
def is_liked_by(resource, user):
    if user in resource.liked_by.all():
        return True
    return False
