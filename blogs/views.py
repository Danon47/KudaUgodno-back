from rest_framework import permissions, viewsets
from rest_framework.exceptions import APIException, PermissionDenied

from blogs.models import Article, ArticleImage, Category, Tag
from blogs.serializers import ArticleImageSerializer, CategorySerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с категориями статей.
    Поддерживаемые методы HTTP:GET, POST, PUT, PATCH, DELETE.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с тегами статей.
    Поддерживаемые методы HTTP:GET, POST, PUT, PATCH, DELETE.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы со статьями.
    Поддерживаемые методы HTTP:GET, POST, PUT, PATCH, DELETE.
    """

    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    from rest_framework.exceptions import APIException

    def get_queryset(self):
        """Переопределяет queryset для фильтрации по параметру is_published."""
        queryset = Article.objects.all()

        # Фильтрация по публикации
        is_published = self.request.query_params.get("is_published")
        if is_published is not None:
            try:
                is_published = is_published.lower() == "true"
                queryset = queryset.filter(is_published=is_published)
            except ValueError as err:  # <-- дали имя исходной ошибке
                raise APIException(
                    "Неверный формат параметра is_published. Используйте true или false."
                ) from err  # <-- добавили  «from err»

        # Фильтрация по возрастанию и убыванию (по количеству просмотров)
        popularity = self.request.query_params.get("popularity", None)
        if popularity:
            if popularity not in ["asc", "desc"]:
                raise APIException("Неверный формат параметра popularity. Используйте 'asc' или 'desc'.")
            queryset = queryset.order_by("-views_count" if popularity == "desc" else "views_count")

        # Фильтрация по стране
        country = self.request.query_params.get("country", None)
        if country:
            try:
                countries = [c.strip() for c in country.split(",")]
                queryset = queryset.filter(countries__name__in=countries)
            except Exception as err:  # можно сузить до ValueError
                raise APIException(f"Ошибка фильтрации по стране: {err}") from err  # <-- ключевое добавление

        user = self.request.user
        if user.is_superuser:  # Если суперпользователь, разрешаем доступ ко всему
            return queryset

        return queryset.filter(author=user)  # Только статьи текущего пользователя

    def perform_create(self, serializer):
        """
        Автоматически устанавливает автора статьи в момент создания.
        """

        serializer.save(author=self.request.user)  # Автор статьи - текущий пользователь

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет существующую статью.  Заменяет все данные статьи данными из запроса.
        Доступно только автору статьи или суперпользователю.
        """

        instance = self.get_object()
        if instance.author != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать эту статью.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет существующую статью. Обновляет только указанные в запросе поля.
        Доступно только автору статьи или суперпользователю.
        """

        instance = self.get_object()
        if instance.author != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать эту статью.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет существующую статью.
        Доступно только автору статьи или суперпользователю.
        """

        instance = self.get_object()
        if instance.author != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете удалить эту статью.")
        return super().destroy(request, *args, **kwargs)


class ArticleImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с изображениями статей
    Поддерживаемые методы HTTP:GET, POST, PUT, PATCH, DELETE.
    """

    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
