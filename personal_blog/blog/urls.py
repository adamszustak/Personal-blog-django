from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HtmlToPdfView, PostDetailView, post_list

app_name = "blog"

urlpatterns = [
    path("", post_list, name="home"),
    path("<slug:slug>", PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:category_slug>", post_list, name="post_category",),
    path("search/", post_list, name="filter_post"),
    path("tag/<slug:tag_slug>", post_list, name="tag_post"),
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
