from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        # fields = ('title', 'content', 'author', 'slug', 'status')
        exclude = ('created', 'updated')

    def validate_title(self, value):
        filter_list = ['java', 'python', 'javascript']
        for i in filter_list:
            if i in value:
                raise serializers.ValidationError(f'dont use !{i}')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'