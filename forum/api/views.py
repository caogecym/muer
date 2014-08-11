from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from forum.models import Post, Tag, Comment
from forum.api.serializers import PostSerializer, TagSerializer, CommentSerializer, UserSerializer


class PostViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        Handles list level url permissions
        '''
        # unlogged in users can only GET
        if request.user and not request.user.is_authenticated():
            return request.method == 'GET'
        # logged in users can GET and POST
        else:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        Handles object level url permissions
        '''
        # any user can GET a detail of a post
        if request.method in ['GET']:
            return True
        # staff have all permissions
        elif request.user and request.user.is_staff:
            return True
        # only logged in user can self PUT, DELETE
        else:
            return request.user == obj.author
        
            
class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes= [PostViewPermission]

    @action(permission_classes=[AllowAny])
    def like(self, request, pk=None):
        post = self.get_object()
        user = self.request.user

        if len(post.liked_by.filter(id=user.id)) == 0 and user.is_authenticated():
            post.liked_by.add(user)

        post.like_count += 1
        post.save()
        return Response({'status': 'post liked'})

    @action()
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = self.request.user

        if user.is_authenticated():
            post.like_count -= 1
            if len(post.liked_by.filter(id=user.id)) > 0:
                post.liked_by.remove(user)
            post.save()
            return Response({'status': 'post unliked'})
        else:
            return Response({'status': 'have to login to unlike'}, status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
