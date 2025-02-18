from django.db import models
from all_fixture.fixture_views import NULLABLE


class RoomUnavailable(models.Model):
    """
    Недоступность номера
    """

    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="unavailables",
        verbose_name="Номер",
        help_text="Номер, который недоступен",
        **NULLABLE
    )
    reason = models.CharField(
        verbose_name="Причина недоступности номера",
        help_text="Причина недоступности номера",
        max_length=100,
    )
    start_date = models.DateField(
        verbose_name="Дата начала действия недоступности номера",
        help_text="Дата начала действия недоступности номера",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания действия недоступности номера",
        help_text="Дата окончания действия недоступности номера",
    )

    class Meta:
        verbose_name = "Недоступность номера"
        verbose_name_plural = "Недоступности номеров"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.reason} ({self.start_date} - {self.end_date})"
