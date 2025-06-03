from django.contrib import admin

from blogs.models import Article, ArticleImage, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель для модели Category"""

    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    search_fields = ("name",)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """Админ панель для модели Tag"""

    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ панель для модели статья"""

    list_display = (
        "title",
        "autor",
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
        "autor",
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


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    """Админ панель для модели фотографии"""

    list_display = ("image", "order")
    list_filter = ("image",)
    search_fields = ("image",)
