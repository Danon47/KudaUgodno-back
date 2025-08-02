from datetime import timedelta

from django.utils import timezone

from users.models import LoginAttempt, User

BAN_STEPS = [
    timedelta(minutes=15),
    timedelta(hours=1),
    timedelta(days=1),
    timedelta(days=7),
]


def record_login_attempt(user: User, success: bool, ip: str | None = None) -> None:
    """Записываем попытку и модифицируем счетчики/бан."""
    LoginAttempt.objects.create(user=user, success=success, ip=ip)

    if success:
        # Сброс
        user.failed_login_count = 0
        user.ban_level = 0
        user.ban_until = None
    else:
        user.failed_login_count += 1
        if user.failed_login_count >= 5:
            # Эскалация
            level = min(user.ban_level, len(BAN_STEPS) - 1)
            user.ban_until = timezone.now() + BAN_STEPS[level]
            user.ban_level = min(level + 1, len(BAN_STEPS) - 1)
            user.failed_login_count = 0
    user.save(update_fields=["failed_login_count", "ban_level", "ban_until"])


def check_ban(user: User):
    """Бросает исключение, если у пользователя активный бан."""
    if user.is_banned():
        raise PermissionError(f"Аккаунт заблокирован до {user.ban_until.strftime('%d.%m.%Y %H:%M')}")
