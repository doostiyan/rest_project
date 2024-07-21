from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ('title', 'content', 'author', 'slug', 'status')
        exclude = ('created', 'updated')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'