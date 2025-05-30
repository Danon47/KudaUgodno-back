from django.db import models


class Article(models.Model):
    """Модель статья"""

    title = models.CharField(max_length=100, verbose_name="Заголовок статьи", help_text="Заголовок статьи")
    autor = models.CharField(max_length=100, verbose_name="Автор статьи")
    content = models.TextField(verbose_name="Текст статьи")
    pub_date = models.DateField(verbose_name="когда выложили статью")
    short_description = models.CharField(max_length=250, verbose_name="Краткое описание, для ленты новостей")
    is_published = models.BooleanField(default=False, verbose_name="опубликована ли статья")
    views_count = models.PositiveIntegerField(default=0, verbose_name="счетчик просмотров")
    rating = models.FloatField(default=0, verbose_name="оценка статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at", "-created_at"]

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    """Модель фотографии к статье"""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/post/")
    order = models.PositiveIntegerField(default=0)  # Поле для указания порядка отображения изображений в статье

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.article.title}"
