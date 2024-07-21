from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from blog.models import Article


# Create your views here.
class ArticleListView(ListView):
    def get_queryset(self):
        return Article.objects.filter(status=True)


class ArticleDetailView(DetailView):
    def get_object(self, *args, **kwargs):
        article = get_object_or_404(Article.objects.filter(status=True), pk=self.kwargs['pk'])
        return article
