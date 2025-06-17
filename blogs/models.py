from django.contrib.auth import get_user_model
from django.db import models

from all_fixture.fixture_views import NULLABLE


class Category(models.Model):
    """Модель категории для статей блога"""

    name_category = models.CharField(max_length=50, verbose_name="Название категории", help_text="Название категории")
    slug_category = models.SlugField(
        max_length=50, unique=True, verbose_name="Slug категории", help_text="Slug категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name_category"]

    def __str__(self):
        return self.name_category


class Tag(models.Model):
    """Модель тега для статей блога"""

    name_tag = models.CharField(max_length=50, verbose_name="Название тега", help_text="Название тега")
    slug_tag = models.SlugField(max_length=50, unique=True, verbose_name="Slug тега", help_text="Slug тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name_tag"]

    def __str__(self):
        return self.name_tag


class Country(models.Model):
    """Модель страна"""

    name_country = models.CharField(
        max_length=100, unique=True, verbose_name="Название страны", help_text="Название страны"
    )
    slug_country = models.SlugField(
        max_length=100, unique=True, verbose_name="Slug страны", help_text="Название страны", default=""
    )

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["name_country"]

    def __str__(self):
        return self.name_country


class Theme(models.Model):
    """Модель тема статьи."""

    name_theme = models.CharField(max_length=100, unique=True, verbose_name="Название темы", help_text="Название темы")
    slug_theme = models.SlugField(max_length=100, unique=True, verbose_name="Название темы", help_text="Название темы")

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["name_theme"]

    def __str__(self):
        return self.name_theme


class Article(models.Model):
    """Модель статья"""

    title = models.CharField(
        max_length=100, verbose_name="Заголовок статьи", help_text="Заголовок статьи (максимум 100 символов)"
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
    is_moderated = models.BooleanField(default=False, verbose_name="Прошла модерацию", help_text="Прошла модерацию")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, **NULLABLE, verbose_name="категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    countries = models.ManyToManyField(Country, blank=True, verbose_name="Страны")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор статьи", **NULLABLE)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Тема статьи")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-pub_date", "-created_at"]
        # permissions = ["can_edit_article", "Может редактировать статью"]

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    """Модель фотографии к статье"""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/post/")
    order = models.PositiveIntegerField(default=0)  # Поле для указания порядка отображения изображений в статье

    class Meta:
        verbose_name = "Изображение статьи"
        verbose_name_plural = "Изображения для статьи"
        ordering = ["order"]

    def __str__(self):
        return f"Изображение для {self.article.title}"
