from django.db import models
from django_filters import (
    CharFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from rest_framework.exceptions import APIException

from all_fixture.choices import CountryChoices
from blogs.models import Article, Theme


class ArticleFilter(FilterSet):
    """Набор фильтров для списка статей."""

    date_from = DateFilter(
        field_name="published_at",
        lookup_expr="gte",
        label="Дата от (ГГГГ-ММ-ДД)",
        method="filter_date_from",
        help_text="Статьи, опубликованные после указанной даты",
    )
    date_to = DateFilter(
        field_name="published_at",
        lookup_expr="lte",
        label="Дата до (ГГГГ-ММ-ДД)",
        method="filter_date_to",
        help_text="Статьи, опубликованные до указанной даты",
    )
    """
    # Закрыла, поскольку универсальный параметр `ordering` уже позволяет сортировать по просмотрам
    # (через `views_count` / `-views_count`), отдельный фильтр `popularity` становится избыточным.
    # если все же нужен, не забыть про импорт ChoiceFilter
    popularity = ChoiceFilter(
        choices=[("asc", "По возрастанию"), ("desc", "По убыванию")],
        method="filter_popularity",
        label="Сортировка по популярности",
        help_text="Сортировка по популярности : asc — меньше просмотров → больше; desc — наоборот",
    )
    """
    country = CharFilter(
        method="filter_country",
        label="Страны (русские названия)",
        help_text="CSV-список русских названий стран",
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

    # ─────────────────────────── Дата публикации ────────────────────────────

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

    # ────────────────────────── Популярность / просмотры ─────────────────────

    @staticmethod
    def filter_popularity(queryset, name, value):  # noqa: ARG003
        if value == "asc":
            return queryset.order_by("views_count")
        if value == "desc":
            return queryset.order_by("-views_count")
        raise APIException("popularity должен быть 'asc' или 'desc'.")

    # ─────────────────────────────── Страна ──────────────────────────────────

    @staticmethod
    def filter_country(queryset, name, value):  # noqa: ARG003
        try:
            name_to_code = {name: code for code, name in CountryChoices.choices}
            codes, unknown = [], []
            for raw in value.split(","):
                ru = raw.strip()
                code = name_to_code.get(ru)
                if code:
                    codes.append(code)
                else:
                    unknown.append(ru)
            if unknown:
<<<<<<< HEAD
                raise APIException(f"Неизвестные страны: {', '.join(unknown)}") from None

            # `countries` — ArrayField(CharField) => lookup contains list-intersection
=======
                raise APIException(f"Неизвестные страны: {', '.join(unknown)}")
>>>>>>> e5cf967 ([~]: рефактор фильтров статей)
            return queryset.filter(countries__contains=codes)
        except Exception as err:
            raise APIException(f"Ошибка фильтрации по стране: {err}") from err

    # ─────────────────────────────── Тема ────────────────────────────────────

    def filter_theme(self, queryset, name, value):  # noqa: ARG003
        if not Theme.objects.filter(id=value).exists():
            raise APIException("Тема с указанным ID не найдена.")
        return queryset.filter(theme_id=value)

    # ─────────────────────────── Права доступа ──────────────────────────────

    @property
    def qs(self):
        """
        анонимы — только published+moderated,
        авторы — свои черновики + published,
        суперпользователь — все.
        """
        base = super().qs
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return base.filter(is_published=True, is_moderated=True)
        if user.is_superuser:
<<<<<<< HEAD
            return base_qs

        # автор — свои + опубликованные
        return base_qs.filter(models.Q(is_published=True, is_moderated=True) | models.Q(author=user))
=======
            return base
        return base.filter(models.Q(is_published=True, is_moderated=True) | models.Q(author=user))
>>>>>>> e5cf967 ([~]: рефактор фильтров статей)
