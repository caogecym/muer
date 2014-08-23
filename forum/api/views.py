from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from forum.api.permissions import PostViewPermission, TagViewPermission, CommentViewPermission, UserViewPermission
from forum.models import Post, Tag, Comment
from forum.api.serializers import PostSerializer, TagSerializer, CommentSerializer, UserSerializer


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
    permission_classes= [TagViewPermission]

class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes= [CommentViewPermission]

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes= [UserViewPermission]
