from datetime import datetime

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.response import Response

from blogs.models import Article, ArticleImage, Category, Tag, Theme
from blogs.serializers import (
    ArticleImageSerializer,
    ArticleSerializer,
    CategorySerializer,
    TagSerializer,
)
from blogs.tasks import send_moderation_notification

# ─────────────────────────── вспом. функции / permissions ──────────────────────────


def _check_permissions(request, instance) -> None:
    """Разрешаем изменение/удаление только автору либо суперпользователю."""
    if instance.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("Вы не можете редактировать или удалять эту статью.")


# ────────────────────────────────── ViewSets ──────────────────────────────────────


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint категорий статей."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint тегов статей."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint статей."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    # ───────────────────────── фильтрация списка статей ───────────────────────────

    def get_queryset(self):  # noqa: C901
        """
        Поддерживаемые query-параметры:
        • date_from / date_to  – диапазон публикации (YYYY-MM-DD);
        • popularity=asc|desc  – сортировка по просмотрам;
        • country              – список стран через запятую;
        • theme_id             – ID темы;
        • обычному пользователю показываем только опубликованные и проверенные статьи.
        """
        queryset = Article.objects.all()

        # 1️⃣ дата публикации
        date_filters: dict[str, datetime] = {}
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        try:
            if date_from:
                date_filters["pub_date__gte"] = datetime.strptime(date_from, "%Y-%m-%d").date()
            if date_to:
                date_filters["pub_date__lte"] = datetime.strptime(date_to, "%Y-%m-%d").date()
            if date_filters:
                queryset = queryset.filter(**date_filters)
        except ValueError as err:
            raise APIException("Неверный формат параметра даты. Используйте YYYY-MM-DD.") from err

        # 2️⃣ популярность
        popularity = self.request.query_params.get("popularity")
        if popularity:
            if popularity not in {"asc", "desc"}:
                raise APIException("Неверный формат popularity. Используйте 'asc' или 'desc'.")
            queryset = queryset.order_by("-views_count" if popularity == "desc" else "views_count")

        # 3️⃣ страна
        country = self.request.query_params.get("country")
        if country:
            try:
                countries = [c.strip() for c in country.split(",")]
                queryset = queryset.filter(countries__name__in=countries)
            except ValueError as err:
                raise APIException(f"Ошибка фильтрации по стране: {err}") from err

        # 4️⃣ тема
        theme_id_param = self.request.query_params.get("theme_id")
        if theme_id_param:
            try:
                theme_id = int(theme_id_param)
            except ValueError as err:
                raise APIException("Неверный формат theme_id. Используйте целое число.") from err

            if not Theme.objects.filter(id=theme_id).exists():
                raise APIException("Тема с указанным ID не найдена.") from None

            queryset = queryset.filter(theme_id=theme_id)

        # 5️⃣ права доступа к списку
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(is_published=True, is_moderated=True)

    # ───────────────────────────── CRUD-overrides ─────────────────────────────

    def perform_create(self, serializer):
        """
        • Автор — текущий пользователь.
        • Статья создаётся как неопубликованная и немодерированная.
        • Отправляем задачу на уведомление модераторов.
        """
        article = serializer.save(author=self.request.user, is_published=False, is_moderated=False)
        send_moderation_notification.delay(article.id)

    def update(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        _check_permissions(request, self.get_object())
        return super().destroy(request, *args, **kwargs)

    # ───────────────────────────── actions ────────────────────────────────

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def moderate(self, request, pk=None):
        """Админ помечает статью как проверенную и опубликованную."""
        article = self.get_object()
        article.is_moderated = True
        article.is_published = True
        article.save(update_fields=["is_moderated", "is_published"])
        return Response({"message": "Статья успешно проверена"}, status=status.HTTP_200_OK)


class ArticleImageViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint изображений статей."""

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
