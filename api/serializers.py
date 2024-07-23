from django.contrib.auth import get_user_model
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from blog.models import Article


class AuthorSerializer( serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ArticleSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    # author = serializers.HyperlinkedIdentityField(view_name='api:authors-detail')  # hyperlink
    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
        }

    author = serializers.SerializerMethodField('get_author')

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

