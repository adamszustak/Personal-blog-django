from django.shortcuts import get_object_or_404

from rest_framework import mixins, views, viewsets

from ..models import Comment, ReplyComment
from .serializers import CommentSerializer, ReplyCommentSerializer


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
