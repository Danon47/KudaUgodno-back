from django.contrib import admin

from blogs.models import Article, ArticleImage, Category, Comment, CommentLike, Country, Tag, Theme


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель для модели Category"""

    list_display = ("name_category", "slug_category")
    list_filter = ("name_category", "slug_category")
    search_fields = ("name_category",)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """Админ панель для модели Tag"""

    list_display = ("name_tag", "slug_tag")
    list_filter = ("name_tag", "slug_tag")
    search_fields = ("name_tag",)


@admin.register(Country)
class ModelCountryAdmin(admin.ModelAdmin):
    """Админ панель для модели Country"""

    list_display = ("name_country", "slug_country")
    list_filter = ("name_country", "slug_country")
    search_fields = ("name_country",)


@admin.register(Theme)
class ModelThemeAdmin(admin.ModelAdmin):
    """Админ панель для модели Theme"""

    list_display = ("name_theme", "slug_theme")
    list_filter = ("name_theme", "slug_theme")
    search_fields = ("name_theme",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ панель для модели статья"""

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
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ панель для модели комментарии"""

    list_display = ("article", "author", "created_at", "is_active")
    list_filter = ("is_active", "article")
    search_fields = ("text", "author__username")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "is_like", "created_at")
    list_filter = ("is_like",)
    search_fields = ("user__username", "comment__text")


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    """Админ панель для модели фотографии"""

    list_display = ("image", "order")
    list_filter = ("image",)
    search_fields = ("image",)
