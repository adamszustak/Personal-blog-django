from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ("field", "title", "created_on", "status", "show_url")
    list_filter = ("status",)
    search_fields = [
        "title",
        "tags",
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("show_url",)

    def show_url(self, instance):
        try:
            url = reverse("post_detail", kwargs={"slug": instance.slug})
            response = format_html(f"<a href={url}>{url}</a>")
            return response
        except NoReverseMatch:
            return None

    show_url.short_description = "Post Url"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
