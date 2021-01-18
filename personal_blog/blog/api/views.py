from django.shortcuts import get_object_or_404

from rest_framework import renderers, response, viewsets
from rest_framework.decorators import action

from ..models import Category, Post
from .serializers import (
    AdvancedPostSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        elif self.action == "retrieve":
            return CategoryDetailSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published.all()
    serializer_class = AdvancedPostSerializer

    def filter_queryset(self, queryset):
        if self.action == "list":
            self.filterset_fields = ("title",)
        return super().filter_queryset(queryset)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def content(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        content = post.content
        return response.Response(content)
