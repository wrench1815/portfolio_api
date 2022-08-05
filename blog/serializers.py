from rest_framework import serializers

from .models import Post

from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        depth = 1


class PostCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['date_posted']
