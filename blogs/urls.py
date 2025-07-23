from rest_framework import routers

from blogs.apps import BlogsConfig
from blogs.views import (
    ArticleImageViewSet,
    ArticleViewSet,
    CategoryViewSet,
    CommentLikeViewSet,
    CommentViewSet,
    TagViewSet,
    ThemeViewSet,
)

app_name = BlogsConfig.name

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"themes", ThemeViewSet, basename="theme")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"comment-likes", CommentLikeViewSet, basename="comment-like")
router.register(r"article-images", ArticleImageViewSet, basename="article-image")

urlpatterns = router.urls
