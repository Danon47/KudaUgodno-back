from rest_framework import serializers
from rest_framework.fields import (
    BooleanField,
    CharField,
    CurrentUserDefault,
    ImageField,
    ListField,
)
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from all_fixture.choices import CountryChoices
from all_fixture.validators.validators import ForbiddenWordValidator
from blogs.models import (
    Article,
    ArticleImage,
    Category,
    Comment,
    CommentLike,
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
    """Реакция (лайк / дизлайк) на комментарий."""

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "is_like", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    """Комментарий с вложенными ответами (до 2-го уровня) и счётчиками реакций."""

    author = StringRelatedField(read_only=True)
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
    """Статья со связанными сущностями и поддержкой русских названий стран."""

    images = ArticleImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # страны приходят/уходят как список русских названий
    countries = ListField(
        child=CharField(),
        required=False,
        help_text="Список русских названий стран (например, ['Россия', 'США'])",
    )

    author = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    theme = PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=True)
    is_published = BooleanField(read_only=True)
    is_moderated = BooleanField(read_only=True)

    # запрет на некорректные слова
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].validators.append(ForbiddenWordValidator(["title"]))
        self.fields["content"].validators.append(ForbiddenWordValidator(["content"]))

    # ───────── countries helpers ─────────

    @staticmethod
    def validate_countries(value):
        """Проверка, что все названия стран валидны (по Russian name)."""
        valid_names = {name for _, name in CountryChoices.choices}
        invalid = [name for name in value if name not in valid_names]
        if invalid:
            raise serializers.ValidationError(f"Неизвестные страны: {', '.join(invalid)}")
        return value

    def to_internal_value(self, data):
        """Преобразуем русские названия в коды перед сохранением."""
        if "countries" in data:
            name_to_code = {name: code for code, name in CountryChoices.choices}
            data["countries"] = [name_to_code[n] for n in data["countries"] if n in name_to_code]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """Преобразуем коды в русские названия при отдаче данных."""
        rep = super().to_representation(instance)
        if "countries" in rep:
            code_to_name = dict(CountryChoices.choices)
            rep["countries"] = [code_to_name.get(code, code) for code in rep["countries"]]
        return rep

    class Meta:
        model = Article
        fields = [
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
            "countries",
            "theme",
            "author",
            "images",
            "comments",
        ]
        read_only_fields = [
            "id",
            "is_published",
            "is_moderated",
            "views_count",
            "rating",
            "created_at",
            "updated_at",
            "images",
            "comments",
        ]
