from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HtmlToPdfView, PostDetailView, post_list

app_name = "blog"

urlpatterns = [
    path("", cache_page(60 * 60 * 12)(post_list), name="home"),
    path("<slug:slug>", PostDetailView.as_view(), name="post_detail"),
    path(
        "category/<slug:category_slug>",
        cache_page(60 * 60 * 12)(post_list),
        name="post_category",
    ),
    path("search/", cache_page(60 * 60 * 12)(post_list), name="filter_post"),
    path(
        "tag/<slug:tag_slug>",
        cache_page(60 * 60 * 12)(post_list),
        name="tag_post",
    ),
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
