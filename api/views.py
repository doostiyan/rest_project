from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Question
from api.permissions import IsSuperUser, IsStaffOrReadOnly, IsAuthorOrReadOnly, IsSuperUserOrStaffReadOnly
from api.serializers import ArticleSerializer, UserSerializer, AuthorSerializer, QuestionSerializer
from blog.models import Article


# class ArticleListView(ListCreateAPIView):
#     # def get_queryset(self):
#     #     print('---------------------')
#     #     print(self.request.user)
#     #     print('---------------------')
#     #     print(self.request.auth) # token
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#
# class ArticleDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsStaffOrReadOnly, IsAuthorOrReadOnly)
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     # lookup_field = 'slug'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ['status', 'author__username']
    search_fields = ['title', 'author__username', 'content', 'author__first_name', 'author__last_name']
    ordering_fields = ['status', 'publish']

    # def get_queryset(self): # فیلتر کردن بر اساس query params
    #     queryset = Article.objects.all()
    #
    #     status = self.request.query_params.get('status')
    #     if status is not None:
    #         queryset = queryset.filter(status=status)
    #     return queryset
    #
    #     author = self.request.query_params.get('author')
    #     if author is not None:
    #         queryset = queryset.filter(author__username=author)
    #     return queryset

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsStaffOrReadOnly]
        else:
            permission_classes = [IsStaffOrReadOnly, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]


# class UserListView(ListCreateAPIView):
#     permission_classes = (IsSuperUserOrStaffReadOnly,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsSuperUserOrStaffReadOnly,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class RevokeToken(APIView): # remove token 
#     permission_classes = (IsAuthenticated,)
#
#     def delete(self, request):
#         request.auth.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrStaffReadOnly, ]


# class AuthorRetrieve(RetrieveAPIView):                    # hyperlink
#     queryset = get_user_model().objects.filter(is_staff=True)
#     serializer_class = AuthorSerializer


class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        ser_data = QuestionSerializer(instance=questions, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        ser_data = QuestionSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsStaffOrReadOnly, IsAuthorOrReadOnly]

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        ser_data = QuestionSerializer(instance=question,data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsStaffOrReadOnly, IsAuthorOrReadOnly]

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)