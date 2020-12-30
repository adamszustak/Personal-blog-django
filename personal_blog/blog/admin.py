from django.contrib import admin
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html

from .models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "field", "created_on", "status", "show_url")
    list_filter = ("status",)
    search_fields = [
        "title",
        "tags",
    ]
    readonly_fields = ("show_url",)
    date_hierarchy = "created_on"

    def show_url(self, instance):
        try:
            url = reverse("blog:post_detail", kwargs={"slug": instance.slug})
            response = format_html(f"<a href={url}>{url}</a>")
            return response
        except NoReverseMatch:
            return None

    show_url.short_description = "Post Url"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
