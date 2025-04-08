from rest_framework.serializers import CharField, ModelSerializer

from insurances.models import InsuranceMedical, InsuranceNotLeaving, Insurances


class InsuranceSerializer(ModelSerializer):
    """
    Сериализатор для модели Insurances (Страховки)
    """

    medical = CharField(source="medical.name", required=True, help_text="Медицинская страховка")
    not_leaving = CharField(
        source="not_leaving.name", required=False, allow_blank=True, help_text="Страховка от невыезда"
    )

    class Meta:
        model = Insurances
        fields = ("id", "medical", "not_leaving")

    def to_representation(self, instance):
        """Выводим названия страховок или None."""
        representation = super().to_representation(instance)
        representation["medical"] = instance.medical.name
        representation["not_leaving"] = instance.not_leaving.name if instance.not_leaving else None
        return representation

    def create(self, validated_data):
        """Создаём запись, если not_leaving не указан — оставляем NULL."""
        medical_name = validated_data.pop("medical")["name"]
        medical_insurance, _ = InsuranceMedical.objects.get_or_create(name=medical_name)

        # Обрабатываем not_leaving, если оно передано
        not_leaving_data = validated_data.pop("not_leaving", None)
        not_leaving_insurance = None
        if not_leaving_data and not_leaving_data["name"]:  # Проверяем, что имя не пустое
            not_leaving_insurance, _ = InsuranceNotLeaving.objects.get_or_create(name=not_leaving_data["name"])

        insurance = Insurances.objects.create(
            medical=medical_insurance, not_leaving=not_leaving_insurance, **validated_data
        )
        return insurance

    def update(self, instance, validated_data):
        """Обновляем запись, учитывая необязательность not_leaving."""
        if "medical" in validated_data:
            medical_name = validated_data.pop("medical")["name"]
            instance.medical, _ = InsuranceMedical.objects.get_or_create(name=medical_name)

        if "not_leaving" in validated_data:
            not_leaving_data = validated_data.pop("not_leaving")
            if not_leaving_data["name"]:  # Если имя передано — создаём/находим объект
                instance.not_leaving, _ = InsuranceNotLeaving.objects.get_or_create(name=not_leaving_data["name"])
            else:  # Если передана пустая строка — очищаем поле
                instance.not_leaving = None

        return super().update(instance, validated_data)
