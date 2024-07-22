from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsSuperUser, IsStaffOrReadOnly, IsAuthorOrReadOnly, IsSuperUserOrStaffReadOnly
from api.serializers import ArticleSerializer, UserSerializer
from blog.models import Article


# class ArticleListView(ListCreateAPIView):
#     # def get_queryset(self):
#     #     print('---------------------')
#     #     print(self.request.user)
#     #     print('---------------------')
#     #     print(self.request.auth)
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

    # def get_queryset(self):
    #     queryset = Article.objects.all()
    #
    #     # status = self.request.query_params.get('status')
    #     # if status is not None:
    #     #     queryset = queryset.filter(status=status)
    #     # return queryset
    #     #
    #     # author = self.request.query_params.get('author')
    #     # if author is not None:
    #     #     queryset = queryset.filter(author__username=author)
    #     # return queryset


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


# class RevokeToken(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def delete(self, request):
#         request.auth.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrStaffReadOnly, ]
