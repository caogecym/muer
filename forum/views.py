from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from forum.models import Post
import random

def index(request):
    latest_post_list = random.sample(Post.objects.all(), 5)
    #latest_joke_list = Post.objects.all()[:5]
    context = {'latest_joke_list': latest_joke_list}
    return render(request, 'index.html', context)

def content(request, joke_id):
    return HttpResponse("You're looking at the content of joke %s." % joke_id)

def like(request, joke_id):
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

    liked_joke = Post.objects.filter(id=joke_id)[0]
    if liked_joke is not None:
        liked_joke.like_count += 1
        response_data['success'] = 1
        response_data['message'] = 'The post has been liked already'
        liked_joke.save()

    data = simplejson.dumps(response_data)
    return HttpResponse(data, mimetype='application/json')
