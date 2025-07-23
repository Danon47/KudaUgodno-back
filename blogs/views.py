from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response

from all_fixture.choices import CountryChoices
from blogs.filters import ArticleFilter
from blogs.models import (
    Article,
    ArticleImage,
    Category,
    Comment,
    CommentLike,
    Tag,
    Theme,
)
from blogs.permissions import IsAuthorOrAdmin
from blogs.serializers import (
    ArticleImageSerializer,
    ArticleSerializer,
    CategorySerializer,
    CommentLikeSerializer,
    CommentSerializer,
    TagSerializer,
    ThemeSerializer,
)
from blogs.tasks import send_moderation_notification

# ──────────────────────────── ViewSets справочников ────────────────────────────


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint категорий статей."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint тегов статей."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint тем статей.

    Права доступа:
    • list / retrieve – доступны всем;
    • create – только авторизованным;
    • update / partial_update / destroy – автор темы либо администратор.
    """

    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    # базовый класс — заменяем динамически
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated()]
        # update / partial_update / destroy
        return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        # если в модели Theme есть поле author, можно раскомментировать:
        # serializer.save(author=self.request.user)
        serializer.save()


# ───────────────────────────── основная сущность ────────────────────────────────


class ArticleViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint статей.

    Фильтрация через `ArticleFilter`:
      • date_from / date_to  — интервал публикации (YYYY-MM-DD)
      • popularity           — asc / desc
      • country              — CSV-список стран (рус. названия)
      • theme_id             — ID темы
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filterset_class = ArticleFilter
    permission_classes = [IsAuthenticated]  # базовый уровень, детально уточняется ниже

    # ─────────────────────── выборка с учётом статуса ───────────────────────────

    def get_queryset(self):
        qs = self.filter_queryset(super().get_queryset())
        user = self.request.user
        return qs if user.is_superuser else qs.filter(is_published=True, is_moderated=True)

    # ───────────────────────────── permissions matrix ───────────────────────────

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            classes = [IsAuthorOrAdmin]
        elif self.action == "create":
            classes = [IsAuthenticated]
        else:
            classes = [AllowAny]
        return [cls() for cls in classes]

    # ─────────────────────────────── CRUD-overrides ─────────────────────────────

    def perform_create(self, serializer):
        """Сохраняем автора, помечаем статью как черновик и уведомляем модераторов."""
        article = serializer.save(
            author=self.request.user,
            is_published=False,
            is_moderated=False,
        )
        send_moderation_notification.delay(article.id)

    # ─────────────────────────── вспом. проверка прав ───────────────────────────

    @staticmethod
    def _check_owner(request, instance):
        if instance.author != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать или удалять эту статью.")

    def update(self, request, *args, **kwargs):
        self._check_owner(request, self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_owner(request, self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_owner(request, self.get_object())
        return super().destroy(request, *args, **kwargs)

    # ───────────────────────────── доп. действия ────────────────────────────────

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def moderate(self, request, pk=None):
        """Админ помечает статью как прошедшую модерацию и опубликованную."""
        article = self.get_object()
        article.is_moderated = True
        article.is_published = True
        article.save(update_fields=["is_moderated", "is_published"])
        return Response({"message": "Статья успешно проверена"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def available_countries(self, request):
        """Возвращает список всех доступных стран (русские названия)."""
        return Response([name for _, name in CountryChoices.choices])


# ───────────────────────── комментарии и реакции ───────────────────────────────


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint комментариев (чтение всем, запись авторизованным)."""

    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint лайков/дизлайков к комментариям."""

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request: Request = self.request
        try:
            comment_id = int(request.data["comment"])
            is_like = bool(request.data.get("is_like", True))
        except (KeyError, ValueError) as err:
            raise ValidationError("Требуется JSON: {'comment': int, 'is_like': bool}") from err

        # заменяем возможную прежнюю реакцию пользователя
        CommentLike.objects.filter(user=request.user, comment_id=comment_id).delete()
        serializer.save(user=request.user, comment_id=comment_id, is_like=is_like)


# ─────────────────────────── изображения статьи ────────────────────────────────


class ArticleImageViewSet(viewsets.ModelViewSet):
    """CRUD-endpoint изображений статей."""

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
