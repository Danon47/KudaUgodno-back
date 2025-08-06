# ─── текущие константы ─────────────────────────────────────────────────────────
MAX_MEDIA_PER_ARTICLE = 10
MAX_FILE_SIZE = 10 * 1024 * 1024  # в байтах (10 МБ)
ALLOWED_VIDEO_EXT = {".mp4", ".webm"}

# ─── алиасы !!!СЫЕРИТЬ!!! с views_fixture.py ────────────────────────────────────
# Максимальное число фото/видео
MAX_PHOTOS = MAX_MEDIA_PER_ARTICLE
MAX_VIDEOS = MAX_MEDIA_PER_ARTICLE

# Максимальный размер в мегабайтах
MAX_PHOTO_SIZE_MB = MAX_FILE_SIZE // (1024 * 1024)  # == 10
MAX_VIDEO_SIZE_MB = MAX_PHOTO_SIZE_MB  # тоже 10 МБ

# Длительность видео (секунд)
MAX_VIDEO_DURATION = 2 * 60  # <-- например (какое нужно в действительности число секунд?)
