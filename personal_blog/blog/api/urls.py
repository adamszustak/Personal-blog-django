from django.urls import include, path

from .views import (
    CategoryDetailView,
    CategoryListView,
    PostContentView,
    PostDetailView,
)

app_name = "api"

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "post/<int:pk>/content/",
        PostContentView.as_view(),
        name="post_content",
    ),
]
