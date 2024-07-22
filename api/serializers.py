from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ('title', 'content', 'author', 'slug', 'status')
        exclude = ('created', 'updated')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'