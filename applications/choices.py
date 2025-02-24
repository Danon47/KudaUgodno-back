from django.db import models


class StatusChoices(models.TextChoices):
    """
    Выбор статуса для заявки
    """

    CONFIRM = "Подтвержден", "Подтвержден"
    AWAIT_CONFIRM = "Ожидает подтверждения", "Ожидает подтверждения"
    NEED_CONTACT = "Необходимо связаться", "Необходимо связаться"
