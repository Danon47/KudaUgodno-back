import django_filters
from rest_framework.exceptions import APIException

from blogs.models import Article, Theme


class ArticleFilter(django_filters.FilterSet):
    """Фильтры для списка статей."""

    date_from = django_filters.DateFilter(
        field_name="pub_date",
        lookup_expr="gte",
        label="Дата от (ГГГГ-ММ-ДД)",
        method="filter_date_from",
        help_text="Фильтр статей, опубликованных после указанной даты",
    )
    date_to = django_filters.DateFilter(
        field_name="pub_date",
        lookup_expr="lte",
        label="Дата до (ГГГГ-ММ-ДД)",
        method="filter_date_to",
        help_text="Фильтр статей, опубликованных до указанной даты",
    )
    popularity = django_filters.ChoiceFilter(
        choices=[("asc", "По возрастанию"), ("desc", "По убыванию")],
        method="filter_popularity",
        label="Сортировка по популярности",
        help_text="Сортировка по количеству просмотров (asc/desc)",
    )
    country = django_filters.CharFilter(
        method="filter_country",
        label="Страны (через запятую)",
        help_text="Фильтр по странам (названия через запятую)",
    )
    theme_id = django_filters.NumberFilter(
        field_name="theme",
        method="filter_theme",
        label="ID темы",
        help_text="Фильтр по ID темы",
    )

    class Meta:
        model = Article
        fields: list[str] = []

    # ─────────────────────────── дата публикации ────────────────────────────

    @staticmethod
    def filter_date_from(queryset, name, value):  # noqa: ARG003
        """Статьи от указанной даты (YYYY-MM-DD)."""
        try:
            return queryset.filter(pub_date__gte=value)
        except ValueError as err:
            raise APIException("Неверный формат даты. Используйте YYYY-MM-DD.") from err

    @staticmethod
    def filter_date_to(queryset, name, value):  # noqa: ARG003
        """Статьи до указанной даты (YYYY-MM-DD)."""
        try:
            return queryset.filter(pub_date__lte=value)
        except ValueError as err:
            raise APIException("Неверный формат даты. Используйте YYYY-MM-DD.") from err

    # ────────────────────────── популярность / просмотры ─────────────────────────

    @staticmethod
    def filter_popularity(queryset, name, value):  # noqa: ARG003
        """Сортировка по количеству просмотров."""
        if value == "asc":
            return queryset.order_by("views_count")
        if value == "desc":
            return queryset.order_by("-views_count")
        raise APIException("popularity должен быть 'asc' или 'desc'.") from None

    # ─────────────────────────────── страна ──────────────────────────────────

    @staticmethod
    def filter_country(queryset, name, value):  # noqa: ARG003
        """Фильтрация по списку стран (CSV)."""
        try:
            countries = [c.strip() for c in value.split(",")]
            return queryset.filter(countries__name__in=countries)
        except Exception as err:  # noqa: BLE001
            raise APIException(f"Ошибка фильтрации по стране: {err}") from err

    # ─────────────────────────────── тема ────────────────────────────────────

    def filter_theme(self, queryset, name, value):  # noqa: ARG003
        """Фильтрация по теме статьи."""
        if not Theme.objects.filter(id=value).exists():
            raise APIException("Тема с указанным ID не найдена.") from None
        return queryset.filter(theme_id=value)

    # ─────────────────────────── права доступа ──────────────────────────────

    @property
    def qs(self):
        """
        Обычным пользователям показываем только опубликованные
        и прошедшие модерацию статьи; админы видят всё.
        """
        qs = super().qs
        user = self.request.user
        return qs if user.is_superuser else qs.filter(is_published=True, is_moderated=True)
