from rest_framework import serializers

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

# ───────────────────────────── базовые сериализаторы ─────────────────────────────


class CategorySerializer(serializers.ModelSerializer):
    """Категория статьи."""

    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Тег статьи."""

    class Meta:
        model = Tag
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    """Страна статьи."""

    class Meta:
        model = Country
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    """Тема статьи."""

    class Meta:
        model = Theme
        fields = "__all__"


class ArticleImageSerializer(serializers.ModelSerializer):
    """Фото статьи."""

    class Meta:
        model = ArticleImage
        fields = "__all__"


# ───────────────────────────── комментарии и лайки ──────────────────────────────


class CommentLikeSerializer(serializers.ModelSerializer):
    """Лайк или дизлайк к комментарию."""

    class Meta:
        model = CommentLike
        fields = "__all__"
        read_only_fields = ("user", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    """Комментарий к статье, рекурсивно выводит ответы и лайки."""

    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    # ───────── helpers ─────────

    def get_replies(self, obj):
        """Вложенные ответы."""
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data

    def get_likes_count(self, obj):
        return obj.likes.filter(is_like=True).count()

    def get_dislikes_count(self, obj):
        return obj.likes.filter(is_like=False).count()


# ───────────────────────────── основной сериализатор ────────────────────────────


class ArticleSerializer(serializers.ModelSerializer):
    """Статья."""

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
        # запрещённые слова
        self.fields["title"].validators.append(ForbiddenWordValidator(["title"]))
        self.fields["content"].validators.append(ForbiddenWordValidator(["content"]))

    class Meta:
        model = Article
        fields = "__all__"
