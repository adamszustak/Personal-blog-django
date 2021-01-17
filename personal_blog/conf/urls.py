from django.conf import settings
from django.conf.urls import handler404
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from blog.sitemaps import CategorySitemap, PostSitemap

sitemaps = {"posts": PostSitemap, "categories": CategorySitemap}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("law/", include("terms_conditions.urls", namespace="terms")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("api/", include("blog.api.urls", namespace="api")),
    re_path("djga/", include("google_analytics.urls")),
]

handler404 = "blog.views.error_404"


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
