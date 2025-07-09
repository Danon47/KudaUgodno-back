from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from blogs.filters import ArticleFilter
from blogs.models import (
    Article,
    ArticleImage,
    Category,
    Comment,
    CommentLike,
    Country,
    Tag,
    Theme,
)
from blogs.serializers import (
    ArticleImageSerializer,
    ArticleSerializer,
    CategorySerializer,
    CommentLikeSerializer,
    CommentSerializer,
    CountrySerializer,
    TagSerializer,
    ThemeSerializer,
)
from blogs.tasks import send_moderation_notification

# ─────────────────────────── вспомогательная функция ────────────────────────────


def _check_permissions(request, instance) -> None:
    """Разрешаем изменение/удаление только автору либо суперпользователю."""
    if instance.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("Вы не можете редактировать или удалять эту статью.")


# ─────────────────────────────────── ViewSets ────────────────────────────────────


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint категорий статей."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint тегов статей."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint стран (чтение всем, изменение авторизованным)."""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ThemeViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint тем статей (только админ)."""

    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAdminUser]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint статей.

    Фильтрация через `ArticleFilter`:
    • date_from / date_to  — диапазон публикации (YYYY-MM-DD)
    • popularity=asc|desc  — сортировка по просмотрам
    • country              — список стран через запятую
    • theme_id             — ID темы
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilter
    queryset = Article.objects.all()

    # ─────────────────────── доп. логика выборки ────────────────────────────────

    def get_queryset(self):
        """Фильтруем, затем скрываем неопубликованное от обычных пользователей."""
        qs = self.filter_queryset(super().get_queryset())
        user = self.request.user
        return qs if user.is_superuser else qs.filter(is_published=True, is_moderated=True)

    # ───────────────────────────── CRUD-overrides ───────────────────────────────

    def perform_create(self, serializer):
        """
        • Автор — текущий пользователь.
        • Статья создаётся как неопубликованная и немодерированная.
        • Уведомляем модераторов асинхронной задачей.
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

    # ───────────────────────────── дополнительные действия ──────────────────────

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def moderate(self, request, pk=None):
        """Админ помечает статью как проверенную и опубликованную."""
        article = self.get_object()
        article.is_moderated = True
        article.is_published = True
        article.save(update_fields=["is_moderated", "is_published"])
        return Response({"message": "Статья успешно проверена"}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint комментариев (чтение всем, запись авторизованным)."""

    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint реакций (лайк/дизлайк) на комментарии."""

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request: Request = self.request
        try:
            comment_id = int(request.data["comment"])
            is_like = bool(request.data.get("is_like", True))
        except (KeyError, ValueError) as err:
            raise ValidationError("Требуется JSON: {'comment': int, 'is_like': bool}") from err

        # заменяем предыдущую реакцию пользователя
        CommentLike.objects.filter(user=request.user, comment_id=comment_id).delete()
        serializer.save(user=request.user, comment_id=comment_id, is_like=is_like)


class ArticleImageViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint изображений статей."""

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
