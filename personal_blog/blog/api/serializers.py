from comments.api.serializers import CommentSerializer
from rest_framework import serializers

from ..models import Category, Post


class CategoryListSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    post_set = serializers.HyperlinkedRelatedField(
        many=True, view_name="api:posts-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "post_count", "post_set"]

    def get_post_count(self, obj):
        return obj.published_post.count()


# Inner serializer for CategoryDetail
class BasicPostSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField(source="field.name")
    author = serializers.ReadOnlyField(source="author.username")
    content = serializers.HyperlinkedIdentityField(
        view_name="api:posts-content", format="html"
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "field_name",
            "title",
            "content",
            "slug",
            "author",
            "created_on",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class CategoryDetailSerializer(CategoryListSerializer):
    post_set = BasicPostSerializer(many=True)


class AdvancedPostSerializer(BasicPostSerializer):
    comments = CommentSerializer(many=True)
    img_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            ["id", "img_url"]
            + BasicPostSerializer.Meta.fields
            + ["comments", "tags"]
        )

    def get_img_url(self, obj):
        return obj.get_image

    def get_tags(self, obj):
        return obj.tags.values_list("name", flat=True)
