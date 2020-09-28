from django.contrib.sitemaps import Sitemap

from .models import Category, Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.created_on


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()
