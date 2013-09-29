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
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from markdown import markdown
from forum.models import Post
from forum.forms import PostForm
import random

def index(request, tag_name=None):
    #if len(Post.objects.all()) >= 3:
    #   post_list = random.sample(Post.objects.all(), 3)
    #else:
    #   post_list = None
    #post_list = [Post.objects.all().filter(id=45)[0]]
    if tag_name is None:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.all().filter(tags__name = tag_name)

    paginator = Paginator(post_list, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts,
               'user': request.user,
              }
    return render(request, 'index.html', context)

def tags(request):
    context = {
               'user': request.user,
              }
    return render(request, 'tags.html', context)

def tag(request, tag):
    return index(request, tag_name=tag)

@login_required
def add_post(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            text = form.cleaned_data['content']
            html = markdown(text)
            post = Post(title=form.cleaned_data['title'], content=html,
                        author=request.user, tagnames=form.cleaned_data['tagnames'])
            post.save()
            return HttpResponseRedirect('/') 
    else:
        # An unbound form
        form = PostForm() 

    return render(request, 'new_post.html', {
        'form': form,
    })

def content(request, post_id):
    post = Post.objects.all().filter(id=post_id)[0]
    context = {'post': post,
               'user': request.user,
              }
    return render(request, 'post.html', context)

def ajax_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        json = simplejson.dumps({ 'not_authenticated': 1 })
        return HttpResponse(json, mimetype='application/json')
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap

@ajax_login_required
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
        "message": '',
        "not_authenticated": 0,
    }

    post_to_like = Post.objects.filter(id=post_id)[0]
    if post_to_like is not None:
        # cancel
        if post_to_like.liked_by.all().filter(username=request.user.username).count() > 0:
            liked_user = post_to_like.liked_by.all().filter(username=request.user.username)[0]
            post_to_like.liked_by.remove(liked_user)
            response_data['status'] = 1
            post_to_like.like_count -= 1
            response_data['message'] = 'The like of post has been canceled'
        # like
        else:
            post_to_like.like_count += 1
            post_to_like.liked_by.add(request.user)
            response_data['message'] = 'The post has been liked by user %s' % request.user.username

        post_to_like.save()
        response_data['success'] = 1

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
