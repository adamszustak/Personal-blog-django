from django.contrib import admin

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ("field", "title", "created_on", "status")
    list_filter = ("status",)
    search_fields = [
        "title", "tags",
    ]
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
