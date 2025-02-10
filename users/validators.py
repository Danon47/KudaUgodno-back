from rest_framework import serializers

class ForbiddenWordValidator:
    """Валидатор для проверки запрещённых слов в текстовых полях."""

    FORBIDDEN_WORDS = {"запрещенное_слово", "недопустимое_имя"}

    def __call__(self, value):
        for word in self.FORBIDDEN_WORDS:
            if word in value.lower():
                raise serializers.ValidationError(f"Введено недопустимое слово: '{word}'")
