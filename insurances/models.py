from django.db import models

from all_fixture.choices import TypeInsuranceChoices
from all_fixture.fixture_views import NULLABLE


class Insurances(models.Model):
    medical = models.CharField(
        choices=TypeInsuranceChoices.choices,
        default="",
        verbose_name="Медицинская страховка",
        help_text="Медицинская страховка",
        **NULLABLE,
    )
    not_leaving = models.CharField(
        choices=TypeInsuranceChoices.choices,
        default="",
        verbose_name="Страховка от невыезда",
        help_text="Страховка от невыезда",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховки"

    def __str__(self):
        return f"{self.medical if self.medical else ''} {self.not_leaving if self.not_leaving else ''}"
