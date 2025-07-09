from rest_framework import routers

from blogs.views import (
    ArticleImageViewSet,
    ArticleViewSet,
    CategoryViewSet,
    CommentLikeViewSet,
    CommentViewSet,
    CountryViewSet,
    TagViewSet,
    ThemeViewSet,
)

app_name = "blogs"

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"countries", CountryViewSet, basename="country")
router.register(r"themes", ThemeViewSet, basename="theme")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"comment-likes", CommentLikeViewSet, basename="comment-like")
router.register(r"article-images", ArticleImageViewSet, basename="article-image")

urlpatterns = router.urls
