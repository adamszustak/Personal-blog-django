from blog.models import Post
from rest_framework import serializers

from ..models import Comment, ReplyComment


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "author", "created_date"]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.published.all())
    replies = ReplyCommentSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ["id", "text", "created_date", "post", "replies", "author"]
