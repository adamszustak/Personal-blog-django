from django.shortcuts import get_object_or_404

from rest_framework import generics, renderers, views
from rest_framework.response import Response

from ..models import Category, Post
from .serializers import (
    AdvancedPostSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filterset_fields = ("name",)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = AdvancedPostSerializer


class PostContentView(views.APIView):
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        content = post.content
        return Response(content)
