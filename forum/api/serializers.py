from rest_framework import serializers
from django.contrib.auth.models import User
from forum.models import Post, Tag, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

