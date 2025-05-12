from django.db import models

from all_fixture.fixture_views import NULLABLE
from users.models import User


class RoomRules(models.Model):
    """Правила в номере"""

    name = models.CharField(
        max_length=100,
        verbose_name="Правила в номере",
        help_text="Правила в номере",
        **NULLABLE,
    )
    option = models.BooleanField(
        verbose_name="Да/Нет",
        help_text="Да/Нет",
        default=False,
    )
    created_by = models.ForeignKey(User, verbose_name="Создана пользователем", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = "Правило в номере"
        verbose_name_plural = "Правила в номерах"
        ordering = ("name",)

    def __str__(self):
        return self.name
