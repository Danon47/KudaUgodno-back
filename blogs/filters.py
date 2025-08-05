from django.db import models
from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from django_filters.filters import BooleanFilter
from rest_framework.exceptions import APIException

from all_fixture.choices import CountryChoices
from blogs.models import Article, ArticleMedia, Theme


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
        """
        Принимает CSV из русских названий стран и фильтрует по их кодам.
        """
        try:
            name_to_code = {name: code for code, name in CountryChoices.choices}
            codes = []
            unknown = []
            for raw in value.split(","):
                name_ru = raw.strip()
                code = name_to_code.get(name_ru)
                if code:
                    codes.append(code)
                else:
                    unknown.append(name_ru)

            if unknown:
                raise APIException(f"Неизвестные страны: {', '.join(unknown)}") from None

            return queryset.filter(countries__contains=codes)
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
        Возвращает queryset с учётом прав доступа:

        • анонимы — только опубликованные и промодерированные статьи;
        • обычные пользователи — опубликованные + свои черновики;
        • администраторы — весь список.
        """
        base_qs = super().qs
        user = getattr(self.request, "user", None)

        # аноним или отсутствие request.user
        if user is None or not user.is_authenticated:
            return base_qs.filter(is_published=True, is_moderated=True)

        # админ видит всё
        if user.is_superuser:
            return base_qs

        # автор — свои + опубликованные
        return base_qs.filter(models.Q(is_published=True, is_moderated=True) | models.Q(author=user))


class ArticleMediaFilter(FilterSet):
    """
    Фильтры для медиа статей
    """

    is_cover = BooleanFilter(
        field_name="is_cover",
        help_text="Фильтр по обложкам (true/false)",
    )

    media_type = ChoiceFilter(
        method="filter_by_type",
        choices=[("photo", "Фото"), ("video", "Видео")],
        help_text="Тип медиа: photo или video",
    )

    class Meta:
        model = ArticleMedia
        fields = ["article", "is_cover"]

    def filter_by_type(self, queryset, name, value):
        """
        Кастомный фильтр по типу медиа
        """

        if value == "photo":
            return queryset.filter(photo__isnull=False)
        elif value == "video":
            return queryset.filter(video__isnull=False)
        return queryset
