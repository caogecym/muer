from django.contrib.auth.models import User

from rest_framework import serializers
from forum.models import Post, Tag, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'content', 'tags', 'post_comments', 'deleted', 'like_count', 'params')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'author', 'like_count')
