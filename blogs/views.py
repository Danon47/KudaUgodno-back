from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
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
from all_fixture.views_fixture import (
    ARTICLE_COUNTRY,
    ARTICLE_DATE_FROM,
    ARTICLE_DATE_TO,
    ARTICLE_ID,
    ARTICLE_MEDIA_ID,
    ARTICLE_THEME_ID,
    BLOG_SETTINGS,
    LIMIT,
    MEDIA_TYPE,
    OFFSET,
)
from blogs.constants import (
    MAX_PHOTO_SIZE_MB,
    MAX_PHOTOS,
    MAX_VIDEO_DURATION,
    MAX_VIDEO_SIZE_MB,
    MAX_VIDEOS,
)
from blogs.filters import ArticleFilter, ArticleMediaFilter
from blogs.models import (
    Article,
    ArticleMedia,
    Category,
    Comment,
    CommentLike,
    Tag,
    Theme,
)
from blogs.permissions import IsAuthorOrAdmin
from blogs.serializers import (
    ArticlePhotoSerializer,
    ArticleSerializer,
    ArticleVideoSerializer,
    CategorySerializer,
    CommentLikeSerializer,
    CommentSerializer,
    TagSerializer,
    ThemeSerializer,
)
from blogs.tasks import send_moderation_notification

# ──────────────────────────── ViewSets справочников ────────────────────────────


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint категорий статей.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint тегов статей.
    """

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
        serializer.save()


# ───────────────────────────── основная сущность ────────────────────────────────


@extend_schema(tags=[BLOG_SETTINGS["name"]])
@extend_schema_view(
    list=extend_schema(
        summary="Список статей",
        description="Получение списка статей с пагинацией и фильтрацией по дате, стране и теме.",
        parameters=[
            LIMIT,
            OFFSET,
            ARTICLE_DATE_FROM,
            ARTICLE_DATE_TO,
            OpenApiParameter(
                name="popularity",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Сортировка по популярности (asc/desc)",
                enum=["asc", "desc"],
                required=False,
            ),
            ARTICLE_COUNTRY,
            ARTICLE_THEME_ID,
        ],
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer(many=True),
                description="Успешное получение списка статей",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание статьи",
        description="Создание новой статьи (автоматически назначается текущий пользователь как автор)",
        request=ArticleSerializer,
        responses={
            201: OpenApiResponse(
                response=ArticleSerializer,
                description="Статья успешно создана",
            ),
            400: OpenApiResponse(
                description="Ошибки валидации",
                examples=[
                    OpenApiExample(
                        "Пример ошибки",
                        value={
                            "title": ["Обязательное поле."],
                            "content": ["Содержит запрещенные слова."],
                        },
                    )
                ],
            ),
            401: OpenApiResponse(description="Требуется аутентификация"),
        },
    ),
    retrieve=extend_schema(
        summary="Детали статьи",
        description="Получение полной информации о статье с комментариями и изображениями",
        parameters=[ARTICLE_ID],
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer,
                description="Успешное получение статьи",
            ),
            404: OpenApiResponse(description="Статья не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление статьи",
        description="Обновление всех полей статьи (только для автора или админа)",
        parameters=[ARTICLE_ID],
        request=ArticleSerializer,
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer,
                description="Статья успешно обновлена",
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
            403: OpenApiResponse(description="Нет прав для редактирования"),
            404: OpenApiResponse(description="Статья не найдена"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление статьи",
        description="Обновление отдельных полей статьи (только для автора или админа)",
        parameters=[ARTICLE_ID],
        request=ArticleSerializer,
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer,
                description="Статья успешно обновлена",
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
            403: OpenApiResponse(description="Нет прав для редактирования"),
            404: OpenApiResponse(description="Статья не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление статьи",
        description="Удаление статьи (только для автора или админа)",
        parameters=[ARTICLE_ID],
        responses={
            204: OpenApiResponse(
                description="Статья успешно удалена",
            ),
            403: OpenApiResponse(description="Нет прав для удаления"),
            404: OpenApiResponse(description="Статья не найдена"),
        },
    ),
    moderate=extend_schema(
        summary="Модерация статьи",
        description="Пометить статью как прошедшую модерацию (только для админа)",
        parameters=[ARTICLE_ID],
        responses={
            200: OpenApiResponse(
                description="Статья успешно промодерирована",
                examples=[OpenApiExample("Пример ответа", value={"message": "Статья успешно проверена"})],
            ),
            403: OpenApiResponse(description="Требуются права администратора"),
            404: OpenApiResponse(description="Статья не найдена"),
        },
    ),
    available_countries=extend_schema(
        summary="Доступные страны",
        description="Получение списка всех доступных стран для статей",
        responses={
            200: OpenApiResponse(
                description="Список стран",
                examples=[OpenApiExample("Пример ответа", value=["Россия", "США", "Германия"])],
            ),
        },
    ),
)
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

    # ───────────────────── выборка с учётом статуса и фильтров ───────────────────

    def get_queryset(self):
        """
        Применяет ArticleFilter к базовому queryset-у.
        Админ получает полный список,
        остальные — только опубликованные и прошедшие модерацию статьи.
        """

        qs = self.filter_queryset(super().get_queryset())
        user = self.request.user
        return qs if user.is_superuser else qs.filter(is_published=True, is_moderated=True)

    # ─────────────────────────────── CRUD-overrides ─────────────────────────────

    def perform_create(self, serializer):
        """
        Сохраняем автора, помечаем статью как черновик и уведомляем модераторов.
        """

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
        """
        Админ помечает статью как прошедшую модерацию и опубликованную.
        """

        article = self.get_object()
        article.is_moderated = True
        article.is_published = True
        article.save(update_fields=["is_moderated", "is_published"])
        return Response({"message": "Статья успешно проверена"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def available_countries(self, request):
        """
        Возвращает список всех доступных стран (русские названия).
        """

        return Response([name for _, name in CountryChoices.choices])


# ───────────────────────── комментарии и реакции ───────────────────────────────


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint комментариев (чтение всем, запись авторизованным).
    """

    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    """
    CRUD-endpoint лайков/дизлайков к комментариям.
    """

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


@extend_schema(tags=["Медиа статей"])
@extend_schema_view(
    list=extend_schema(
        summary="Список медиафайлов статьи",
        description="Получение списка всех медиафайлов статьи с фильтрацией по типу",
        parameters=[
            LIMIT,
            OFFSET,
            OpenApiParameter(
                name="article",
                type=int,
                description="ID статьи для фильтрации",
                required=False,
            ),
            MEDIA_TYPE,
            OpenApiParameter(
                name="is_cover",
                type=bool,
                description="Фильтр по обложкам (true/false)",
                required=False,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ArticlePhotoSerializer(many=True),
                description="Список медиафайлов",
            )
        },
    ),
    retrieve=extend_schema(
        summary="Детали медиафайла",
        description="Получение полной информации о медиафайле",
        parameters=[ARTICLE_MEDIA_ID],
        responses={
            200: OpenApiResponse(response=ArticlePhotoSerializer, description="Данные медиафайла"),
            404: OpenApiResponse(description="Медиафайл не найден"),
        },
    ),
    create=extend_schema(
        summary="Загрузка нового фото",
        description=f"""
        Загрузка фотографии для статьи. Ограничения:
        - Макс. {MAX_PHOTOS} фото на статью
        - Размер до {MAX_PHOTO_SIZE_MB}MB
        - Форматы: JPG, PNG, GIF
        """,
        request=ArticlePhotoSerializer,
        responses={
            201: OpenApiResponse(response=ArticlePhotoSerializer, description="Фото успешно загружено"),
            400: OpenApiResponse(
                description="Ошибки валидации",
                examples=[
                    OpenApiExample(
                        "Пример ошибки",
                        value={"photo": ["Превышен максимальный размер файла"]},
                    )
                ],
            ),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление фото",
        description="Обновление всех полей фотографии",
        parameters=[ARTICLE_MEDIA_ID],
        request=ArticlePhotoSerializer,
        responses={
            200: OpenApiResponse(response=ArticlePhotoSerializer, description="Фото успешно обновлено"),
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Фото не найдено"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление фото",
        description="Обновление отдельных полей фотографии",
        parameters=[ARTICLE_MEDIA_ID],
        request=ArticlePhotoSerializer,
        responses={
            200: OpenApiResponse(response=ArticlePhotoSerializer, description="Фото успешно обновлено"),
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Фото не найдено"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление фото",
        description="Удаление фотографии из статьи",
        parameters=[ARTICLE_MEDIA_ID],
        responses={
            204: OpenApiResponse(description="Фото успешно удалено"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Фото не найдено"),
        },
    ),
    set_cover=extend_schema(
        methods=["POST"],
        summary="Установка обложки",
        description="Пометить это фото как обложку статьи",
        parameters=[ARTICLE_MEDIA_ID],
        responses={
            200: OpenApiResponse(
                description="Фото успешно установлено как обложка",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={"detail": "Фото успешно установлено как обложка"},
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Ошибка: нельзя сделать видео обложкой",
                examples=[
                    OpenApiExample(
                        "Пример ошибки",
                        value={"detail": "Только фото может быть обложкой"},
                    )
                ],
            ),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Фото не найдено"),
        },
    ),
)
class ArticlePhotoViewSet(viewsets.ModelViewSet):
    """
    API для управления фотографиями статей.
    Доступные действия:
    - list: Получить все фото статьи
    - create: Загрузить новое фото
    - retrieve: Получить конкретное фото
    - update: Обновить фото (включая отметку как обложки)
    - destroy: Удалить фото
    - set_cover: Специальный эндпоинт для установки обложки
    """

    queryset = ArticleMedia.objects.filter(photo__isnull=False)
    serializer_class = ArticlePhotoSerializer
    permission_classes = [AllowAny]
    filterset_class = ArticleMediaFilter

    def perform_create(self, serializer):
        """
        Проверка лимита фото перед сохранением
        """

        article = serializer.validated_data["article"]
        if article.media.filter(photo__isnull=False).count() >= MAX_PHOTOS:
            raise ValidationError({"detail": f"Максимум {MAX_PHOTOS} фото на статью"})
        serializer.save()

    @extend_schema(
        methods=["POST"],
        description="Установить это фото как обложку статьи",
        responses={
            200: OpenApiResponse(description="Фото успешно установлено как обложка"),
            400: OpenApiResponse(description="Это видео или произошла ошибка"),
        },
    )
    @action(detail=True, methods=["post"])
    def set_cover(self, request, pk=None):
        """
        Специальный эндпоинт для установки обложки
        """

        media = self.get_object()

        if not media.photo:
            return Response(
                {"detail": "Только фото может быть обложкой"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Автоматически сбрасываем другие обложки
        ArticleMedia.objects.filter(article=media.article, is_cover=True).exclude(pk=media.pk).update(is_cover=False)

        media.is_cover = True
        media.save()

        return Response(
            {"detail": "Фото успешно установлено как обложка"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Медиа статей"])
@extend_schema_view(
    list=extend_schema(
        summary="Список видео статьи",
        description="Получение списка всех видео статьи",
        parameters=[
            LIMIT,
            OFFSET,
            OpenApiParameter(
                name="article",
                type=int,
                description="ID статьи для фильтрации",
                required=False,
            ),
        ],
        responses={200: OpenApiResponse(response=ArticleVideoSerializer(many=True), description="Список видео")},
    ),
    retrieve=extend_schema(
        summary="Детали видео",
        description="Получение полной информации о видео",
        parameters=[ARTICLE_MEDIA_ID],
        responses={
            200: OpenApiResponse(response=ArticleVideoSerializer, description="Данные видео"),
            404: OpenApiResponse(description="Видео не найдено"),
        },
    ),
    create=extend_schema(
        summary="Загрузка нового видео",
        description=f"""
        Загрузка видео для статьи. Ограничения:
        - Макс. {MAX_VIDEOS} видео на статью
        - Размер до {MAX_VIDEO_SIZE_MB}MB
        - Длительность до {MAX_VIDEO_DURATION} сек
        - Форматы: MP4, MOV, WEBM
        """,
        request=ArticleVideoSerializer,
        responses={
            201: OpenApiResponse(response=ArticleVideoSerializer, description="Видео успешно загружено"),
            400: OpenApiResponse(
                description="Ошибки валидации",
                examples=[
                    OpenApiExample(
                        "Пример ошибки",
                        value={"video": ["Превышена максимальная длительность"]},
                    )
                ],
            ),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление видео",
        description="Обновление всех полей видео",
        parameters=[ARTICLE_MEDIA_ID],
        request=ArticleVideoSerializer,
        responses={
            200: OpenApiResponse(response=ArticleVideoSerializer, description="Видео успешно обновлено"),
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Видео не найдено"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление видео",
        description="Обновление отдельных полей видео",
        parameters=[ARTICLE_MEDIA_ID],
        request=ArticleVideoSerializer,
        responses={
            200: OpenApiResponse(response=ArticleVideoSerializer, description="Видео успешно обновлено"),
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Видео не найдено"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление видео",
        description="Удаление видео из статьи",
        parameters=[ARTICLE_MEDIA_ID],
        responses={
            204: OpenApiResponse(description="Видео успешно удалено"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Видео не найдено"),
        },
    ),
)
class ArticleVideoViewSet(viewsets.ModelViewSet):
    """
    API для управления видео к статьям.
    Доступные действия:
    - list: Получить все видео статьи
    - create: Загрузить новое видео
    - retrieve: Получить конкретное видео
    - update: Обновить информацию о видео
    - destroy: Удалить видео
    """

    queryset = ArticleMedia.objects.filter(video__isnull=False)
    serializer_class = ArticleVideoSerializer
    permission_classes = [AllowAny]
    filterset_class = ArticleMediaFilter

    def perform_create(self, serializer):
        """
        Проверка лимита видео перед сохранением
        """
        article = serializer.validated_data["article"]
        if article.media.filter(video__isnull=False).count() >= MAX_VIDEOS:
            raise ValidationError({"detail": f"Максимум {MAX_VIDEOS} видео на статью"})
        serializer.save()
