from rest_framework import routers

from blogs.views import (
    ArticleImageViewSet,
    ArticleViewSet,
    CategoryViewSet,
    CommentLikeViewSet,
    CommentViewSet,
    TagViewSet,
)

app_name = "blogs"


router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"comment-likes", CommentLikeViewSet, basename="comment-like")
router.register(r"articleimages", ArticleImageViewSet, basename="articleimage")

urlpatterns = router.urls
