from rest_framework import serializers

from all_fixture.validators.validators import ForbiddenWordValidator
from blogs.models import Article, ArticleImage, Category, Country, Tag, Theme


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


class CountrySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Country"""

    class Meta:
        model = Country
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Theme"""

    class Meta:
        model = Theme
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
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), default=None)
    country = CountrySerializer(many=True, read_only=True)

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        self.fields["title"].validators.append(ForbiddenWordValidator(["title"]))
        self.fields["content"].validators.append(ForbiddenWordValidator(["content"]))

    class Meta:
        model = Article
        fields = "__all__"
