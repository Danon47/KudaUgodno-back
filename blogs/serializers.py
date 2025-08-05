from rest_framework import serializers
from rest_framework.fields import (
    BooleanField,
    CharField,
    CurrentUserDefault,
    ListField,
    SerializerMethodField,
)
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from all_fixture.choices import CountryChoices
from blogs.models import (
    Article,
    ArticleMedia,
    Category,
    Comment,
    CommentLike,
    Tag,
    Theme,
)
from blogs.validators import (
    DynamicForbiddenWordValidator,
    validate_media_file_size,
    validate_photo_count,
    validate_video_count,
)

# ───────────────────────────── базовые справочники ──────────────────────────────


class CategorySerializer(serializers.ModelSerializer):
    """
    Категория статьи.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    """
    Тег статьи.
    """

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ThemeSerializer(serializers.ModelSerializer):
    """
    Тематика статьи.
    """

    class Meta:
        model = Theme
        fields = ["id", "name", "slug"]


# ─────────────────────────── изображения к статье ──────────────────────────────


# class ArticleImageSerializer(serializers.ModelSerializer):
#     """Изображение, прикреплённое к статье."""
#
#     image = ImageField()
#
#     class Meta:
#         model = ArticleImage
#         fields = ["id", "article", "image", "order"]
#         read_only_fields = ["id"]
class ArticlePhotoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки и управления фотографиями статей.
    Поддерживает:
    - Загрузку до 10 фото на статью
    - Отметку фото как обложки
    - Автоматическую валидацию размера и формата
    """

    class Meta:
        model = ArticleMedia
        fields = ["id", "article", "photo", "is_cover", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "article": {"write_only": True},
            "photo": {"help_text": f"Изображение (JPG/PNG/GIF), макс. {ArticleMedia.MAX_PHOTO_SIZE_MB}MB"},
            "is_cover": {"help_text": "Отметьте, чтобы сделать это фото обложкой статьи"},
        }

    def validate(self, data):
        article = data.get("article") or self.instance.article if self.instance else None

        if article:
            validate_photo_count(article)

        if "photo" in data:
            validate_media_file_size(data["photo"])

        return data


class ArticleVideoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки и управления видео к статьям.
    Поддерживает:
    - Загрузку до 3 видео на статью
    - Максимальный размер 50MB и длительность 5 мин
    - Валидацию форматов (MP4, MOV, WEBM)
    """

    class Meta:
        model = ArticleMedia
        fields = ["id", "article", "video", "video_duration", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "article": {"write_only": True},
            "video": {"help_text": f"Видео (MP4/MOV/WEBM), макс. {ArticleMedia.MAX_VIDEO_SIZE_MB}MB"},
            "video_duration": {
                "help_text": "Длительность видео в секундах (макс. 300 сек)",
                "required": True,
            },
        }

    def validate(self, data):
        article = data.get("article") or self.instance.article if self.instance else None

        if article:
            validate_video_count(article)

        if "video" in data:
            validate_media_file_size(data["video"], is_video=True)
            if "video_duration" not in data:
                raise serializers.ValidationError({"video_duration": "Укажите длительность видео в секундах"})

        return data


# ───────────────────────────── комментарии и лайки ──────────────────────────────


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    Реакция (лайк / дизлайк) на комментарий.
    """

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "is_like", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Комментарий с вложенными ответами (до 2-го уровня) и счётчиками реакций.
    """

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
    """
    Статья со связанными сущностями и поддержкой русских названий стран.
    """

    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    cover_image = SerializerMethodField()
    photos = ArticlePhotoSerializer(many=True, read_only=True, source="media.filter(photo__isnull=False)")
    videos = ArticleVideoSerializer(many=True, read_only=True, source="media.filter(video__isnull=False)")

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
        self.fields["title"].validators.append(DynamicForbiddenWordValidator(field_name="title"))
        self.fields["content"].validators.append(DynamicForbiddenWordValidator(field_name="content"))

    # ───────── countries helpers ─────────

    @staticmethod
    def validate_countries(value):
        """
        Проверка, что все названия стран валидны (по Russian name).
        """

        valid_names = {name for _, name in CountryChoices.choices}
        invalid = [name for name in value if name not in valid_names]
        if invalid:
            raise serializers.ValidationError(f"Неизвестные страны: {', '.join(invalid)}")
        return value

    def to_internal_value(self, data):
        """
        Преобразуем русские названия в коды перед сохранением.
        """

        if "countries" in data:
            name_to_code = {name: code for code, name in CountryChoices.choices}
            data["countries"] = [name_to_code[n] for n in data["countries"] if n in name_to_code]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Преобразуем коды в русские названия при отдаче данных.
        """

        rep = super().to_representation(instance)
        if "countries" in rep:
            code_to_name = dict(CountryChoices.choices)
            rep["countries"] = [code_to_name.get(code, code) for code in rep["countries"]]
        return rep

    def get_cover_image(self, obj):
        """
        Возвращает URL обложки статьи если она есть.
        """

        cover = obj.media.filter(is_cover=True).first()
        if cover and cover.photo:
            request = self.context.get("request")
            return request.build_absolute_uri(cover.photo.url) if request else cover.photo.url
        return None

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
            "cover_image",
            "photos",
            "videos",
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
            "photos",
            "videos",
            "comments",
        ]
