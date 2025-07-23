from django.contrib import admin

from all_fixture.choices import CountryChoices
from blogs.models import Article, ArticleImage, Category, Comment, CommentLike, Tag, Theme


# noinspection PyUnresolvedReferences
class SlugNameAdmin(admin.ModelAdmin):
    """
    Базовый класс админки для моделей с полями name и slug.
    """

    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(SlugNameAdmin):
    """Админ панель для модели Category (наследует SlugNameAdmin)."""


@admin.register(Tag)
class TagsAdmin(SlugNameAdmin):
    """Админ панель для модели Tag."""


@admin.register(Theme)
class ThemeAdmin(SlugNameAdmin):
    """Админ панель для модели Theme."""


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ панель для модели статья."""

    list_display = (
        "title",
        "author",
        "content",
        "pub_date",
        "short_description",
        "is_published",
        "views_count",
        "rating",
        "created_at",
        "updated_at",
        "display_countries",
    )
    list_filter = (
        "title",
        "author",
        "content",
        "pub_date",
        "short_description",
        "is_published",
        "views_count",
        "rating",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "countries",
    )

    def display_countries(self, obj):
        """
        Преобразует коды стран статьи в строку с русскими названиями.
        """

        country_mapping = dict(CountryChoices.choices)
        return ", ".join(country_mapping.get(code, code) for code in obj.countries)

    display_countries.short_description = "Страны"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ панель для модели комментарии."""

    list_display = (
        "article",
        "text",
        "author",
        "created_at",
        "is_active",
        "likes_count_display",
        "dislikes_count_display",
    )
    list_filter = (
        "is_active",
        "article",
        "author",
        "created_at",
    )
    search_fields = ["text"]
    actions = ["approve_comments"]

    def likes_count_display(self, obj):
        """
        Отображение лайков.
        """
        return obj.likes_count

    likes_count_display.short_description = "Лайки"
    likes_count_display.admin_order_field = "likes_count"

    def dislikes_count_display(self, obj):
        """
        Отображение дизлайков.
        """

        return obj.dislikes_count

    dislikes_count_display.short_description = "Дизлайки"
    dislikes_count_display.admin_order_field = "dislikes_count"

    def approve_comments(self, queryset):
        queryset.update(is_active=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """Админ панель для модели лайки/дизлайки к комментариям."""

    list_display = ("comment", "user", "is_like", "created_at")
    list_filter = ("is_like",)


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    """Админ панель для модели фотографии."""

    list_display = ("image", "order")
    list_filter = ("image",)
    search_fields = ("image",)
