# Константы политики медиа для приложения «Блог»
from typing import Final

# Количество
MAX_PHOTOS: Final[int] = 10
MAX_VIDEOS: Final[int] = 1

# Размеры
MAX_FILE_SIZE_MB: Final[int] = 10
MAX_FILE_SIZE_BYTES: Final[int] = MAX_FILE_SIZE_MB * 1024 * 1024  # 10 МБ

# Видео
ALLOWED_VIDEO_EXT: Final[tuple[str, ...]] = (".mp4", ".webm")
MAX_VIDEO_DURATION_SEC: Final[int] = 2 * 60  # 120 секунд
