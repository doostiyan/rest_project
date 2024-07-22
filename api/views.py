from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsSuperUser, IsStaffOrReadOnly, IsAuthorOrReadOnly, IsSuperUserOrStaffReadOnly
from api.serializers import ArticleSerializer, UserSerializer
from blog.models import Article


# Create your views here.
class ArticleListView(ListCreateAPIView):
    # def get_queryset(self):
    #     print('---------------------')
    #     print(self.request.user)
    #     print('---------------------')
    #     print(self.request.auth)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffOrReadOnly, IsAuthorOrReadOnly)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # lookup_field = 'slug'


class UserListView(ListCreateAPIView):
    permission_classes = (IsSuperUserOrStaffReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUserOrStaffReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class RevokeToken(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def delete(self, request):
#         request.auth.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)