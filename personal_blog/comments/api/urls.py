from rest_framework.routers import DefaultRouter

from .views import CommentViewSet

app_name = "api_comment"

router = DefaultRouter()
router.register(r"comment", CommentViewSet)
urlpatterns = router.urls
