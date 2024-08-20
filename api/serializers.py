from django.contrib.auth import get_user_model
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from api.custom_relational_field import UserEmailRelationalField
from api.models import Question, Answer
from blog.models import Article


class AuthorSerializer(serializers.ModelSerializer):
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

    def validate_title(self, value):  # validation serializer داخل تایتل اگه این حرفها بود ارور بده
        filter_list = ['java', 'python', 'javascript']
        for i in filter_list:
            if i in value:
                raise serializers.ValidationError(f'dont use !{i}')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    user = UserEmailRelationalField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def get_answer(self, obj):
        result = obj.answers.all()
        return AnswerSerializer(instance=result, many=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'