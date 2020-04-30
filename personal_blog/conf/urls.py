from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    re_path("djga/", include("google_analytics.urls")),
]
