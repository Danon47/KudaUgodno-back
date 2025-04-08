from django.db import models

from all_fixture.fixture_views import NULLABLE


class InsuranceMedical(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Медицинская страховка", help_text="Название страховой компании"
    )

    class Meta:
        verbose_name = "Медицинская страховка"
        verbose_name_plural = "Медицинские страховки"

    def __str__(self):
        return self.name


class InsuranceNotLeaving(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Страховка от невыезда",
        help_text="Название страховой компании",
    )

    class Meta:
        verbose_name = "Страховка от невыезда"
        verbose_name_plural = "Страховки от невыезда"

    def __str__(self):
        return self.name


class Insurances(models.Model):
    medical = models.ForeignKey(
        InsuranceMedical,
        on_delete=models.CASCADE,
        verbose_name="Медицинская страховка",
        help_text="Медицинская страховка",
    )
    not_leaving = models.ForeignKey(
        InsuranceNotLeaving,
        on_delete=models.SET_NULL,
        verbose_name="Страховка от невыезда",
        help_text="Страховка от невыезда",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховки"

    def __str__(self):
        return f"{self.medical} {self.not_leaving if self.not_leaving else ''}"
