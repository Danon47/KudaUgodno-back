from django.contrib import admin

from all_fixture.choices import CountryChoices
from blogs.models import Article, Category, Comment, CommentLike, MediaAsset, Tag, Theme


class SlugNameAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(SlugNameAdmin):
    pass


@admin.register(Tag)
class TagAdmin(SlugNameAdmin):
    pass


@admin.register(Theme)
class ThemeAdmin(SlugNameAdmin):
    pass


class CountryListFilter(admin.SimpleListFilter):
    title = "Страна"
    parameter_name = "country"

    def lookups(self, request, model_admin):
        return CountryChoices.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(countries__contains=[self.value()])
        return queryset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "views_count",
        "reading_time_minutes",
        "created_at",
        "updated_at",
        "display_countries",
    )
    list_filter = (
        "status",
        "category",
        "theme",
        CountryListFilter,
        "author",
        "created_at",
    )
    search_fields = ("title", "content", "countries")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("tags", "theme", "category")
    list_select_related = ("author", "category", "theme")
    prefetch_related = ("tags",)

    def display_countries(self, obj):
        mapping = dict(CountryChoices.choices)
        return ", ".join(mapping.get(c, c) for c in obj.countries)

    display_countries.short_description = "Страны"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "user",
        "status",
        "created_at",
        "likes_count_display",
        "dislikes_count_display",
    )
    list_filter = ("status", "article", "user", "created_at")
    search_fields = ["text"]
    actions = ["approve_comments"]
    list_select_related = ("article", "user")

    def likes_count_display(self, obj):
        return obj.likes.count()

    likes_count_display.short_description = "Лайки"

    def dislikes_count_display(self, obj):
        return obj.likes.filter(is_like=False).count()

    dislikes_count_display.short_description = "Дизлайки"

    def approve_comments(self, queryset):
        queryset.update(status="approved")

    approve_comments.short_description = "Одобрить выбранные комментарии"


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "is_like", "created_at")
    list_filter = ("is_like",)
    list_select_related = ("comment", "user")


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("article", "type", "file", "order")
    list_filter = ("type", "article")
    search_fields = ("file",)
    list_select_related = ("article",)
