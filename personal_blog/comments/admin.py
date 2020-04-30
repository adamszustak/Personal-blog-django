from django.contrib import admin

from .models import Comment, ReplyComment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_date", "is_approved")
    list_filter = ("is_approved", "created_date")
    search_fields = ("author", "post")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)


class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = (
        "comment",
        "text",
        "created_date",
    )
    list_filter = ("created_date",)
    search_fields = ("comment",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)
