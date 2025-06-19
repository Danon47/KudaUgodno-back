from rest_framework import serializers

from .models import CalendarDate, CalendarPrice


class CategoryPriceCalendarSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = CalendarPrice
        fields = ["room", "price"]


class PriceCalendarSerializer(serializers.ModelSerializer):
    calendar_prices = CategoryPriceCalendarSerializer(
        many=True,
    )

    class Meta:
        model = CalendarDate
        fields = [
            "id",
            "start_date",
            "end_date",
            "available_for_booking",
            "discount",
            "discount_amount",
            "calendar_prices",
        ]

    # def validate(self, data):
    #     # Проверка дат
    #     if data["start_date"] > data["end_date"]:
    #         raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
    #     # Проверка скидки
    #     if data.get("discount") and not data.get("discount_amount"):
    #         raise serializers.ValidationError("Скидка указана, но сумма скидки не указана")
    #     return data

    # def create(self, validated_data):
    #     categories_data = validated_data.pop("category_prices", [])
    #     room = super().create(validated_data)
    #
    #     # Создаем связанные цены категорий
    #     category_objs = [CategoryPriceCalendar(room=room, **cat_data) for cat_data in categories_data]
    #     CategoryPriceCalendar.objects.bulk_create(category_objs)
    #
    #     return room

    #
    # def update(self, instance, validated_data):
    #     categories_data = validated_data.pop("category_prices", [])
    #
    #     # Обновляем основной объект
    #     instance = super().update(instance, validated_data)
    #
    #     # Обновляем связанные объекты
    #     instance.category_prices.all().delete()
    #     category_objs = [CategoryPriceCalendar(room=instance, **cat_data) for cat_data in categories_data]
    #     CategoryPriceCalendar.objects.bulk_create(category_objs)
    #
    #     return instance
