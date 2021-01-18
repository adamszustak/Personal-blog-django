from .views import CommentViewSet

app_name = "api_comment"

# router registered in blog.api.urls
routeList = ((r"comments", CommentViewSet, "comments"),)
