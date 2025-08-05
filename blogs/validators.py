from pathlib import Path

from rest_framework.exceptions import ValidationError

from blogs.constants import MAX_PHOTO_SIZE_MB, MAX_PHOTOS, MAX_VIDEO_SIZE_MB, MAX_VIDEOS


class DynamicForbiddenWordValidator:
    """
    Валидатор, проверяющий наличие запрещенных слов.
    """

    def __init__(self, field_name=None):
        self.field_name = field_name
        self.forbidden_words = self._load_forbidden_words()

    def _load_forbidden_words(self):
        """
        Загружает запрещенные слова из файла
        """

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


def validate_photo_count(article):
    """
    Проверка максимального количества фото
    """

    if article.media.filter(photo__isnull=False).count() >= MAX_PHOTOS:
        raise ValidationError(f"Нельзя загрузить более {MAX_PHOTOS} фото на статью")


def validate_video_count(article):
    """
    Проверка максимального количества видео
    """

    if article.media.filter(video__isnull=False).count() >= MAX_VIDEOS:
        raise ValidationError(f"Нельзя загрузить более {MAX_VIDEOS} видео на статью")


def validate_media_file_size(file, is_video=False):
    """
    Проверка размера файла
    """

    max_size = MAX_VIDEO_SIZE_MB if is_video else MAX_PHOTO_SIZE_MB
    if file.size > max_size * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла: {max_size}MB")
