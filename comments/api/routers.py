from rest_framework.routers import DefaultRouter
from .viewsets import CommentViewSet

router = DefaultRouter()
router.register("comments", CommentViewSet)

urlpatterns = router.urls