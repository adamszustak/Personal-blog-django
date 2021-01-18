from django.urls import path

import comments.api.urls as CommentUrls
from rest_framework import routers

from .views import CategoryViewSet, PostViewSet

app_name = "api"

routeList = (
    (r"categories", CategoryViewSet, "categories"),
    (r"posts", PostViewSet, "posts"),
)

routeLists = (routeList, CommentUrls.routeList)

router = routers.DefaultRouter()
for routeList in routeLists:
    for route in routeList:
        router.register(route[0], route[1], basename=route[2])
urlpatterns = router.urls
