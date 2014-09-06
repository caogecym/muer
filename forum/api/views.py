import django_filters
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import filters

from forum.api.permissions import PostViewPermission, TagViewPermission, CommentViewPermission, UserViewPermission
from forum.models import Post, Tag, Comment
from forum.api.serializers import PostSerializer, TagSerializer, CommentSerializer, UserSerializer


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['author', 'like_count', 'liked_by']


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'like_count', 'liked_by']


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostViewPermission]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PostFilter

    @action(permission_classes=[AllowAny])
    def like(self, request, pk=None):
        post = self.get_object()
        user = self.request.user

        if len(post.liked_by.filter(id=user.id)) == 0 and user.is_authenticated():
            post.liked_by.add(user)

        post.like_count += 1
        post.save()
        return Response({'status': 'post liked'})

    @action(permission_classes=[AllowAny])
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
            return Response({'status': 'have to login to unlike'}, status=status.HTTP_403_FORBIDDEN)

class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagViewPermission]

class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentViewPermission]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CommentFilter

    @action(permission_classes=[AllowAny])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = self.request.user

        if len(comment.liked_by.filter(id=user.id)) == 0:
            if user.is_authenticated():
                comment.liked_by.add(user)
            comment.like_count += 1
            comment.save()
            return Response({'status': 'comment liked', 'id': comment.id})
        else:
            return Response({'status': 'already liked', 'id': comment.id}, status=status.HTTP_403_FORBIDDEN)

    @action(permission_classes=[AllowAny])
    def unlike(self, request, pk=None):
        comment = self.get_object()
        user = self.request.user

        if user.is_authenticated():
            comment.like_count -= 1
            if len(comment.liked_by.filter(id=user.id)) > 0:
                comment.liked_by.remove(user)
            comment.save()
            return Response({'status': 'comment unliked', 'id': comment.id})
        else:
            return Response({'status': 'have to login to unlike'}, status=status.HTTP_403_FORBIDDEN)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]
