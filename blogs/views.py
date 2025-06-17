from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.exceptions import (
    APIException,
    PermissionDenied,
)

from blogs.models import Article, ArticleImage, Category, Tag, Theme
from blogs.serializers import (
    ArticleImageSerializer,
    ArticleSerializer,
    CategorySerializer,
    TagSerializer,
)

# ──────────────────────────── вспомогательные функции ───────────────────────────


def _check_permissions(request, instance) -> None:
    """
    Проверяет, имеет ли пользователь право редактировать или удалять статью.
    """
    if instance.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("Вы не можете редактировать или удалять эту статью.")


# ─────────────────────────────── view-сеты блога ────────────────────────────────


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint для категорий статей."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint для тегов статей."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint для статей."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    # ─────────────────────────── фильтрация списка статей ───────────────────────────

    def get_queryset(self):
        """
        Фильтрация статей по:
        • дате публикации (date_from, date_to);
        • популярности (asc/desc);
        • странам (country);
        • теме (theme_id);
        • автору (если пользователь не суперпользователь).
        """
        queryset = Article.objects.all()

        # 1️⃣ дата публикации
        date_filters = {}
        date_from_param = self.request.query_params.get("date_from")
        date_to_param = self.request.query_params.get("date_to")
        try:
            if date_from_param:
                date_filters["pub_date__gte"] = datetime.strptime(date_from_param, "%Y-%m-%d").date()
            if date_to_param:
                date_filters["pub_date__lte"] = datetime.strptime(date_to_param, "%Y-%m-%d").date()
            if date_filters:
                queryset = queryset.filter(**date_filters)
        except ValueError as err:
            raise APIException("Неверный формат параметра даты. Используйте YYYY-MM-DD.") from err

        # 2️⃣ популярность
        popularity_param = self.request.query_params.get("popularity")
        if popularity_param:
            if popularity_param not in {"asc", "desc"}:
                raise APIException("Неверный формат параметра popularity. Используйте 'asc' или 'desc'.")
            queryset = queryset.order_by("-views_count" if popularity_param == "desc" else "views_count")

        # 3️⃣ страна
        country_param = self.request.query_params.get("country")
        if country_param:
            try:
                countries = [c.strip() for c in country_param.split(",")]
                queryset = queryset.filter(countries__name__in=countries)
            except ValueError as err:
                raise APIException(f"Ошибка фильтрации по стране: {err}") from err

        # 4️⃣ тема
        theme_id_param = self.request.query_params.get("theme_id")
        if theme_id_param:
            try:
                theme_id = int(theme_id_param)
            except ValueError as err:
                raise APIException("Неверный формат параметра theme_id. Используйте числовой ID темы.") from err

            if not Theme.objects.filter(id=theme_id).exists():
                raise APIException("Тема с указанным ID не найдена.") from None

            queryset = queryset.filter(theme_id=theme_id)

        # 5️⃣ права доступа
        user = self.request.user
        return queryset if user.is_superuser else queryset.filter(author=user)

    # ──────────────────────────────── CRUD-overrides ──────────────────────────────

    def perform_create(self, serializer):
        """
        Автоматически проставляет автора и помечает статью
        как неопубликованную и немодерированную.
        """
        serializer.save(
            author=self.request.user,
            is_published=False,
            is_moderated=False,
        )

    # проверки прав перед изменением/удалением
    def update(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().destroy(request, *args, **kwargs)


class ArticleImageViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint для изображений статей."""

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
