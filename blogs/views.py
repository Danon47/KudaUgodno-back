from rest_framework import permissions, viewsets
from rest_framework.exceptions import APIException, PermissionDenied

from blogs.models import Article, ArticleImage, Category, Tag, Theme
from blogs.serializers import (
    ArticleImageSerializer,
    ArticleSerializer,
    CategorySerializer,
    TagSerializer,
)


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

    def get_queryset(self):
        """Фильтрация по публикации, популярности, стране и теме."""
        queryset = Article.objects.all()

        # 1️⃣ публикация
        is_published_param = self.request.query_params.get("is_published")
        if is_published_param is not None:
            try:
                is_published = is_published_param.lower() == "true"
                queryset = queryset.filter(is_published=is_published)
            except ValueError as err:
                raise APIException("Неверный формат параметра is_published. Используйте true или false.") from err

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
                queryset = queryset.filter(theme_id=theme_id)
            except ValueError as err:
                raise APIException("Неверный формат параметра theme_id. Используйте числовой ID темы.") from err
            except Theme.DoesNotExist:
                raise APIException("Тема с указанным ID не найдена.") from None

        # -- права доступа
        user = self.request.user
        return queryset if user.is_superuser else queryset.filter(author=user)

    # ────────────────────────── пермишены на запись ──────────────────────────

    def perform_create(self, serializer):
        """При создании автоматически проставляем автора."""
        serializer.save(author=self.request.user)

    def _check_owner(self, instance, user):
        if instance.author != user and not user.is_superuser:
            raise PermissionDenied("Нет прав изменять/удалять эту статью.")

    def update(self, request, *args, **kwargs):
        self._check_owner(self.get_object(), request.user)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_owner(self.get_object(), request.user)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_owner(self.get_object(), request.user)
        return super().destroy(request, *args, **kwargs)


class ArticleImageViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint для изображений статей."""

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
