from rest_framework import serializers
from rest_framework.fields import (
    ImageField,
)

from all_fixture.validators.validators import ForbiddenWordValidator
from blogs.models import (
    Article,
    ArticleImage,
    Category,
    Comment,
    CommentLike,
    Country,
    Tag,
    Theme,
)

# ───────────────────────────── базовые справочники ──────────────────────────────


class CategorySerializer(serializers.ModelSerializer):
    """Категория статьи."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    """Тег статьи."""

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CountrySerializer(serializers.ModelSerializer):
    """Страна публикации статьи."""

    class Meta:
        model = Country
        fields = ["id", "name", "slug"]


class ThemeSerializer(serializers.ModelSerializer):
    """Тематика статьи."""

    class Meta:
        model = Theme
        fields = ["id", "name", "slug"]


# ─────────────────────────── изображения к статье ──────────────────────────────


class ArticleImageSerializer(serializers.ModelSerializer):
    """Изображение, прикреплённое к статье."""

    image = ImageField()

    class Meta:
        model = ArticleImage
        fields = ["id", "article", "image", "order"]
        read_only_fields = ["id"]


# ───────────────────────────── комментарии и лайки ──────────────────────────────


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    Реакция (лайк / дизлайк) на комментарий.

    Используется для:
    • создания новой реакции (POST);
    • удаления/обновления существующей реакции (DELETE / PATCH).

    Особенности:
    • 1 пользователь → 1 реакция на конкретный комментарий
      (при повторной реакции старая заменяется новой).
    """

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "is_like", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Комментарий с вложенными ответами (до 2-го уровня) и счётчиками реакций.
    """

    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    dislikes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "article",
            "author",
            "parent",
            "text",
            "replies",
            "likes_count",
            "dislikes_count",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "author",
            "replies",
            "likes_count",
            "dislikes_count",
            "created_at",
            "updated_at",
        ]

    # ───────── helpers ─────────

    def get_replies(self, obj):
        """Возвращает вложенные ответы, глубина ≤ 2."""
        depth = self.context.get("depth", 0)
        if depth >= 2:
            return []
        qs = Comment.objects.filter(parent=obj)
        return CommentSerializer(qs, many=True, context={"depth": depth + 1}).data

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.filter(is_like=True).count()

    @staticmethod
    def get_dislikes_count(obj):
        return obj.likes.filter(is_like=False).count()


# ───────────────────────────── основная сущность ────────────────────────────────


class ArticleSerializer(serializers.ModelSerializer):
    """Подробная информация о статье со связанными сущностями."""

    images = ArticleImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    country = CountrySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=True)
    is_published = serializers.BooleanField(read_only=True)
    is_moderated = serializers.BooleanField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Валидаторы на запрещённые слова
        self.fields["title"].validators.append(ForbiddenWordValidator(["title"]))
        self.fields["content"].validators.append(ForbiddenWordValidator(["content"]))

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "pub_date",
            "short_description",
            "is_published",
            "is_moderated",
            "views_count",
            "rating",
            "created_at",
            "updated_at",
            "category",
            "tags",
            "country",
            "theme",
            "author",
            "images",
            "comments",
        )
        read_only_fields = (
            "id",
            "is_published",
            "is_moderated",
            "views_count",
            "rating",
            "created_at",
            "updated_at",
            "images",
            "comments",
        )
