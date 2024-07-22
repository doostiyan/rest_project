from django.urls import path

# from api.views import ArticleListView, ArticleDetailView, UserDetailView, UserListView

app_name = 'api'
# urlpatterns = [
#     path('', ArticleListView.as_view(), name='list'),
#     path('<int:pk>/', ArticleDetailView.as_view(), name='detail'),
#     # path('<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
#     path('users/', UserListView.as_view(), name='user-list'),
#     path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
# ]

from .views import UserViewSet, ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='users'),
router.register('articles', ArticleViewSet, basename='articles'),
urlpatterns = router.urls
