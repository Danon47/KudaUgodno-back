from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Разрешает доступ:
    - Чтение (GET, HEAD, OPTIONS): всем
    - Изменения: только автору или superuser
    - Удаление: только автору или superuser
    """

    def has_object_permission(self, request, view, obj):
        # Для безопасных методов (GET, HEAD, OPTIONS) разрешаем доступ
        if request.method in SAFE_METHODS:
            return True

        if not hasattr(obj, "author"):
            return request.user.is_superuser

        # Для изменений разрешаем только автору или админу
        return obj.author == request.user or request.user.is_superuser
