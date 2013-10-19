import random
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
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

def warning(request):
    context = {
               'user': request.user,
              }
    return render(request, 'warning.html', context)

def home(request):
    context = {
               'user': request.user,
              }
    return render(request, 'home.html', context)

def index(request, tag_name=None, order_by='-added_at'):
    if tag_name is not None:
        posts = Post.objects.filter(tags__name = tag_name)
    else:
        posts = Post.objects

    post_list = posts.order_by(order_by)

    paginator = Paginator(post_list, 10) # Show 10 contacts per page

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

def index_hottest(request):
    return index(request, order_by='-like_count')

def about(request):
    context = {
               'user': request.user,
              }
    return render(request, 'about.html', context)

def tag(request, tag):
    return index(request, tag_name=tag)

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_url = request.GET.copy()
        if query_url.has_key('page'):
            del query_url['page']

        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'content',])
        
        post_list = Post.objects.filter(entry_query).order_by('-added_at')

        paginator = Paginator(post_list, 10) # Show 10 contacts per page

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

    else:
        return HttpResponseRedirect('/home')
    return render_to_response('index.html', { 
                              'query_string': query_string, 
                              'posts': posts,
                              'query': query_url,
                              },
                              context_instance=RequestContext(request))

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
    try:
        post = Post.objects.get(id=post_id)
    except:
        post = None
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
