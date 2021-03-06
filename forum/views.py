import re
import hashlib
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from markdown import markdown
from forum.models import Post, Comment
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
        posts = Post.objects.filter(tags__name=tag_name)
    else:
        posts = Post.objects

    post_list = posts.order_by(order_by).filter(deleted=False)

    paginator = Paginator(post_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
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
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
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
    if ('q' in request.GET) and request.GET['q'].strip():
        query_url = request.GET.copy()
        if 'page' in query_url:
            del query_url['page']

        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'content'])

        post_list = Post.objects.filter(entry_query).order_by('-added_at')

        paginator = Paginator(post_list, 10)  # Show 10 contacts per page

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
def add_post(request, post_id=None):
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        if post.author != request.user:
            return HttpResponseForbidden("Only owner of this post is allowed to edit")
    else:
        post = Post(author=request.user)

    if request.method == 'POST':  # If the form has been submitted...
        form = PostForm(request.POST, instance=post)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            text = form.cleaned_data['content']
            html = markdown(text)
            post.title = form.cleaned_data['title']
            post.content = html
            post.tagnames = form.cleaned_data['tagnames']
            post.save()
            return HttpResponseRedirect('/')
    else:
        # An unbound form
        form = PostForm(instance=post)

    return render(request, 'new_post.html', {
        'form': form,
        'post_id': post_id,
    })

def content(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        post = None
    context = {
        'post': post,
        'user': request.user,
    }
    return render(request, 'post.html', context)

@login_required
def delete_post(request, post_id):
    response_data = {
        "allowed": 1,
        "success": 1,
        "status": 0,
        "message": '',
        "not_authenticated": 0,
    }

    post = Post.objects.get(id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Only owner of this post is allowed to delete")

    if post is not None:
        post.deleted = True
        response_data['message'] = 'The post has been deleted by user %s' % request.user.username

        post.save()
        response_data['success'] = 1

    data = simplejson.dumps(response_data)
    return HttpResponse(data, mimetype='application/json')

def comment_post(request, post_id):
    '''We should assume that comment_data is valid, if it comes to this step'''
    response_data = {
        "allowed": 1,
        "success": 1,
        "message": '',
    }
    post_to_comment = Post.objects.get(id=post_id)
    if post_to_comment is not None:
        comment = Comment(content_object=post_to_comment, author=request.user, content=request.POST['comment_data'])
        comment.save()
        response_data['message'] = 'Comment has been added to post %s by user %s' % (post_id, request.user.username)
        response_data['success'] = 1

    data = simplejson.dumps(response_data)
    return HttpResponse(data, mimetype='application/json')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/posts/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

class Weixin(View):
    token = 'muer_awesome'

    def validate(self, request):
        signature = request.REQUEST.get('signature', '')
        timestamp = request.REQUEST.get('timestamp', '')
        nonce = request.REQUEST.get('nonce', '')

        print 'wechat server info: %s %s %s' % (signature, timestamp, nonce)
        tmp_str = hashlib.sha1(''.join(sorted([self.token, timestamp, nonce]))).hexdigest()
        if tmp_str == signature:
            return True

        return False

    def get(self, request):
        if self.validate(request):
            return HttpResponse(request.REQUEST.get('echostr', ''))

        return HttpResponseForbidden('Wechat handshake failed, please use official testing portal')
