from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.sitemaps.views import sitemap

from django.conf import settings
from django.conf.urls import handler404
from blog.sitemaps import PostSitemap, CategorySitemap


sitemaps = {"posts": PostSitemap, "categories": CategorySitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    re_path("djga/", include("google_analytics.urls")),
]

handler404 = "blog.views.error_404"


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
