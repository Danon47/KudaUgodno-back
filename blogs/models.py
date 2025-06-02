from django.db import models
from all_fixture.fixture_views import NULLABLE


class Category(models.Model):
    """Модель категории для статей блога"""

    name = models.CharField(max_length=50, verbose_name="Название категории", help_text="Название категории")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug категории", help_text="Slug категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тега для статей блога"""

    name = models.CharField(max_length=50, verbose_name="Название тега", help_text="Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug тега", help_text="Slug тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель статья"""

    title = models.CharField(
        max_length=100, verbose_name="Заголовок статьи", help_text="Заголовок статьи (максимум 100 символов)"
    )
    autor = models.CharField(
        max_length=100, verbose_name="Автор статьи", help_text="Автор стать (максимум 100 символов)"
    )
    content = models.TextField(verbose_name="Текст статьи", help_text="Текст статьи")
    pub_date = models.DateField(
        verbose_name="Когда выложили статью", help_text="Когда выложили статью. Формат: ГГГГ-ММ-ДД"
    )
    short_description = models.CharField(
        max_length=250,
        verbose_name="Краткое описание, для ленты новостей",
        help_text="Краткое описание, для ленты новостей (максимум 250 символов)",
    )
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликована ли статья", help_text="Опубликована ли статья"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Счетчик просмотров", help_text="Счетчик просмотров"
    )
    rating = models.FloatField(default=0, verbose_name="Оценка статьи", help_text="Оценка статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", help_text="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения", help_text="Дата последнего изменения"
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, **NULLABLE, verbose_name="категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-pub_date", "-created_at"]

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    """Модель фотографии к статье"""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/post/")
    order = models.PositiveIntegerField(default=0)  # Поле для указания порядка отображения изображений в статье

    class Meta:
        verbose_name = "Изображение статьи"
        verbose_name__plural = "Изображения для статьи"
        ordering = ["order"]

    def __str__(self):
        return f"Изображение для {self.article.title}"
