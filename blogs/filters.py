from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from rest_framework.exceptions import APIException

from blogs.models import Article, Theme


class ArticleFilter(FilterSet):
    """Набор фильтров для списка статей."""

    date_from = DateFilter(
        field_name="pub_date",
        lookup_expr="gte",
        label="Дата от (ГГГГ-ММ-ДД)",
        method="filter_date_from",
        help_text="Статьи, опубликованные после указанной даты",
    )
    date_to = DateFilter(
        field_name="pub_date",
        lookup_expr="lte",
        label="Дата до (ГГГГ-ММ-ДД)",
        method="filter_date_to",
        help_text="Статьи, опубликованные до указанной даты",
    )
    popularity = ChoiceFilter(
        choices=[("asc", "По возрастанию"), ("desc", "По убыванию")],
        method="filter_popularity",
        label="Сортировка по популярности",
        help_text="asc — меньше просмотров → больше; desc — наоборот",
    )
    country = CharFilter(
        method="filter_country",
        label="Страны (CSV)",
        help_text="Список стран через запятую",
    )
    theme_id = NumberFilter(
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
        try:
            return queryset.filter(pub_date__gte=value)
        except ValueError as err:
            raise APIException("Неверный формат даты. Используйте YYYY-MM-DD.") from err

    @staticmethod
    def filter_date_to(queryset, name, value):  # noqa: ARG003
        try:
            return queryset.filter(pub_date__lte=value)
        except ValueError as err:
            raise APIException("Неверный формат даты. Используйте YYYY-MM-DD.") from err

    # ────────────────────────── популярность / просмотры ─────────────────────

    @staticmethod
    def filter_popularity(queryset, name, value):  # noqa: ARG003
        if value == "asc":
            return queryset.order_by("views_count")
        if value == "desc":
            return queryset.order_by("-views_count")
        raise APIException("popularity должен быть 'asc' или 'desc'.") from None

    # ─────────────────────────────── страна ──────────────────────────────────

    @staticmethod
    def filter_country(queryset, name, value):  # noqa: ARG003
        try:
            countries = [c.strip() for c in value.split(",")]
            return queryset.filter(countries__name__in=countries)
        except Exception as err:  # noqa: BLE001
            raise APIException(f"Ошибка фильтрации по стране: {err}") from err

    # ─────────────────────────────── тема ────────────────────────────────────

    def filter_theme(self, queryset, name, value):  # noqa: ARG003
        if not Theme.objects.filter(id=value).exists():
            raise APIException("Тема с указанным ID не найдена.") from None
        return queryset.filter(theme_id=value)

    # ─────────────────────────── права доступа ──────────────────────────────

    @property
    def qs(self):
        """
        Обычным пользователям показываем только опубликованные и
        прошедшие модерацию статьи; администраторы видят всё.
        """
        qs = super().qs
        user = self.request.user
        return qs if user.is_superuser else qs.filter(is_published=True, is_moderated=True)
