from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth

from forum.models import Post
import random

def index(request):
    latest_post_list = random.sample(Post.objects.all(), 5)
    context = {'latest_post_list': latest_post_list,
               'user': request.user,
              }
    return render(request, 'index.html', context)

def content(request, post_id):
    return HttpResponse("You're looking at the content of post %s." % post_id)

def like(request, post_id):
    '''
        vote code:
            status  =  0, By default
                       1, Cancel
    '''
    response_data = {
        "allowed": 1,
        "success": 1,
        "status": 0,
        "count": 0,
        "message": ''
    }

    liked_post = Post.objects.filter(id=post_id)[0]
    if liked_post is not None:
        liked_post.like_count += 1
        response_data['success'] = 1
        response_data['message'] = 'The post has been liked already'
        liked_post.save()

    data = simplejson.dumps(response_data)
    return HttpResponse(data, mimetype='application/json')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/posts/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
