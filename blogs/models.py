from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models

from blogs.constants import (
    MAX_PHOTO_SIZE_MB,
    MAX_PHOTOS,
    MAX_VIDEO_DURATION,
    MAX_VIDEO_SIZE_MB,
    MAX_VIDEOS,
)
from blogs.validators import validate_media_file_size

NULLABLE = {"blank": True, "null": True}


class SlugNameModel(models.Model):
    """
    Абстрактная модель с полями name и slug.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Укажите название, не больше 100 символов",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug",
        help_text="Уникальный идентификатор для URL, не больше 100 символов",
    )

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(SlugNameModel):
    """Модель категории для статей блога."""

    class Meta(SlugNameModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(SlugNameModel):
    """Модель тега для статей блога."""

    class Meta(SlugNameModel.Meta):
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Theme(SlugNameModel):
    """Модель тема статьи."""

    class Meta(SlugNameModel.Meta):
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Article(models.Model):
    """Модель статья."""

    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок статьи",
        help_text="Заголовок статьи (максимум 100 символов)",
    )
    content = models.TextField(
        verbose_name="Текст статьи",
        help_text="Текст статьи",
    )
    pub_date = models.DateField(
        verbose_name="Когда выложили статью",
        help_text="Когда выложили статью. Формат: ГГГГ-ММ-ДД",
    )
    short_description = models.CharField(
        max_length=250,
        verbose_name="Краткое описание, для ленты новостей",
        help_text="Краткое описание, для ленты новостей (максимум 250 символов)",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликована ли статья",
        help_text="Опубликована ли статья",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Счетчик просмотров",
        help_text="Счетчик просмотров",
    )
    rating = models.FloatField(
        default=0,
        verbose_name="Оценка статьи",
        help_text="Оценка статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        help_text="Дата последнего изменения",
    )
    is_moderated = models.BooleanField(
        default=False,
        verbose_name="Прошла модерацию",
        help_text="Прошла модерацию",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="категория",
        help_text="категория",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги",
        help_text="Теги",
    )
    countries = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Страны",
        help_text="Список стран в формате ['Россия', 'Казахстан']",
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Автор статьи",
        **NULLABLE,
        help_text="Автор статьи",
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Тема статьи",
        help_text="Тема статьи",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-pub_date", "-created_at"]

    def __str__(self):
        return self.title

    def user_can_edit(self, user):
        """Проверяет, может ли пользователь редактировать статью"""

        return user.is_staff or self.author == user


class Comment(models.Model):
    """Модель комментария к статье."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Статья",
        help_text="Статья",
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Автор",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="replies",
        verbose_name="Родительский комментарий",
        help_text="Родительский комментарий",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Текст комментария",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата обновления",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Активен",
    )

    @property
    def likes_count(self) -> int:
        return self.likes.filter(is_like=True).count()

    @property
    def dislikes_count(self):
        return self.likes.filter(is_like=False).count()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]  # от новой к старой

    def __str__(self):
        return f"Комментарий от {self.author} к статье '{self.article.title}'"


class CommentLike(models.Model):
    """Лайки/дизлайки к комментариям."""

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="likes",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Комментарии пользователя",
        help_text="Комментарии пользователя",
    )
    is_like = models.BooleanField(
        default=True,
        verbose_name="Лайк (True) / дизлайк (False)",
        help_text="Лайк (True) / дизлайк (False)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания",
        help_text="Дата и время создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления",
        help_text="Дата и время обновления",
    )

    class Meta:
        unique_together = (
            "comment",
            "user",
        )  # Один пользователь — одна реакция на комментарий
        verbose_name = "Лайк комментария"
        verbose_name_plural = "Лайки комментариев"

    def __str__(self):
        return f"{'Лайк' if self.is_like else 'Дизлайк'} от {self.user} к комментарию #{self.comment.id}"


class ArticleMedia(models.Model):
    """
    Модель для медиаконтента статей.
    Поддерживает:
    - До 10 фото на статью (макс. 5MB каждое)
    - До 3 видео на статью (макс. 50MB, до 5 мин)
    - Возможность отметить одно фото как обложку статьи
    """

    MAX_PHOTOS = MAX_PHOTOS
    MAX_VIDEOS = MAX_VIDEOS
    MAX_PHOTO_SIZE_MB = MAX_PHOTO_SIZE_MB
    MAX_VIDEO_SIZE_MB = MAX_VIDEO_SIZE_MB
    MAX_VIDEO_DURATION = MAX_VIDEO_DURATION

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name="Связанная статья",
        help_text="Статья, к которой прикрепляется медиаконтент",
    )
    photo = models.ImageField(
        upload_to="blog/article_photos/%Y/%m/%d/",
        **NULLABLE,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif"],
                message="Допустимы только изображения в форматах JPG, PNG или GIF",
            ),
        ],
        verbose_name="Фотография",
        help_text=f"Загрузите изображение (JPG/PNG/GIF), макс. размер {MAX_PHOTO_SIZE_MB}MB",
    )
    video = models.FileField(
        upload_to="blog/article_videos/%Y/%m/%d/",
        **NULLABLE,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "mov", "webm"],
                message="Допустимы только видео в форматах MP4, MOV или WEBM",
            ),
        ],
        verbose_name="Видеофайл",
        help_text=f"Загрузите видео (MP4/MOV/WEBM), макс. размер {MAX_VIDEO_SIZE_MB}MB, длительность до 5 минут",
    )
    video_duration = models.PositiveIntegerField(
        **NULLABLE,
        validators=[MaxValueValidator(MAX_VIDEO_DURATION)],
        verbose_name="Длительность видео (сек)",
        help_text="Длительность видео в секундах (макс. 300 сек)",
    )
    is_cover = models.BooleanField(
        default=False,
        verbose_name="Обложка статьи",
        help_text="Отметьте, чтобы использовать это фото как обложку статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время загрузки файла",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления",
        help_text="Дата и время обновления",
    )
    # image = models.ImageField(
    #     upload_to="blog/post/",
    #     help_text="место хранения image",
    # )
    # is_video = models.BooleanField(
    #     default=False,
    #     help_text="место хранения is_video",
    # )
    # order = models.PositiveIntegerField(
    #     default=0,
    #     help_text="порядок отображения изображений",
    # )  # Поле для указания порядка отображения изображений в статье

    class Meta:
        verbose_name = "Медиа статьи"
        verbose_name_plural = "Медиа статей"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(photo__isnull=False) | models.Q(video__isnull=False),
                name="photo_or_video_required",
            ),
            models.UniqueConstraint(
                fields=["article", "is_cover"],
                condition=models.Q(is_cover=True),
                name="unique_article_cover",
            ),
        ]

    def __str__(self):
        return f"Медиа #{self.id} для статьи {self.article_id}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.photo and self.video:
            raise ValidationError("Нельзя загружать фото и видео одновременно")

        if self.is_cover and not self.photo:
            raise ValidationError("Обложкой может быть только фотография")

        if self.photo:
            validate_media_file_size(self.photo)

        if self.video:
            validate_media_file_size(self.video, is_video=True)
            if not self.video_duration:
                raise ValidationError("Укажите длительность видео")

    def save(self, *args, **kwargs):
        """
        Автоматически сбрасываем другие обложки при сохранении
        """

        if self.is_cover and self.photo:
            ArticleMedia.objects.filter(article=self.article, is_cover=True).exclude(pk=self.pk).update(is_cover=False)
        super().save(*args, **kwargs)
