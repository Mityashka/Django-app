from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from rest_framework.reverse import reverse_lazy

from .models import Article


class ArticleListView(ListView):
    queryset = (
        Article.objects.filter(published_at__isnull=False).order_by('-published_at')
    )

class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return Article.objects.filter(published_at__isnull=False).order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:200]

    def item_link(self, item):
        return reverse('blogapp:article', kwargs={'pk': item.pk})