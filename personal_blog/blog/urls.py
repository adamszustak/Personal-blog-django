from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    PostList,
    PostDetailView,
    PostCategoryView,
    PostFilterList,
    PostTagView,
    HtmlToPdfView,
)

app_name = "blog"

urlpatterns = [
    path("", PostList.as_view(), name="home"),
    path("<slug:slug>", PostDetailView.as_view(), name="post_detail"),
    path(
        "category/<slug:slug>",
        PostCategoryView.as_view(),
        name="post_category",
    ),
    path("szukaj/", PostFilterList.as_view(), name="filter_post"),
    path("tag/<slug:slug>", PostTagView.as_view(), name="tag_post"),
    path(
        "generate/pdf/<slug:slug>",
        HtmlToPdfView.as_view(),
        name="generate_pdf",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
