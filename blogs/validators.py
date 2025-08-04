from pathlib import Path

from rest_framework.exceptions import ValidationError


class DynamicForbiddenWordValidator:
    """
    Валидатор, проверяющий наличие запрещенных слов.
    """

    def __init__(self, field_name=None):
        self.field_name = field_name
        self.forbidden_words = self._load_forbidden_words()

    def _load_forbidden_words(self):
        """Загружает запрещенные слова из файла"""
        base_dir = Path(__file__).parent
        file_path = Path(r"C:\Users\andre\PycharmProjects\backend\all_fixture\validators\forbidden_words.txt")

        try:
            with open(file_path, encoding="utf-8") as f:
                return [word.strip().lower() for word in f if word.strip()]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл forbidden_words.txt не найден в {base_dir}.") from e

    def __call__(self, value):
        """
        Проверка значения на наличие запрещенных слов
        """

        if isinstance(value, str) and any(word in value.lower() for word in self.forbidden_words):
            raise ValidationError("Введено недопустимое слово")
        return value
