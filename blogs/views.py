from rest_framework import viewsets

from blogs.models import Article, ArticleImage, Category, Tag
from blogs.serializers import ArticleImageSerializer, ArticleSerializer, CategorySerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        is_published = self.request.query_params.get("is_published", None)
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published)
        return queryset


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
