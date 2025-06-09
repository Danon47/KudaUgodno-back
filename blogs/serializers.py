from rest_framework import serializers

from blogs.models import Article, ArticleImage, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории"""

    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Тег"""

    class Meta:
        model = Tag
        fields = "__all__"


class ArticleImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели фотографии к статье"""

    class Meta:
        model = ArticleImage
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели статья"""

    images = ArticleImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = "__all__"
