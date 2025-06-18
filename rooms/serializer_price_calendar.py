from rest_framework import serializers

from .models import CategoryPriceCalendar, PriceCalendar


class CategoryPriceCalendarSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = CategoryPriceCalendar
        fields = ["room_category", "price"]
        extra_kwargs = {"price_calendar": {"required": False}}

    def validate_category_prices(self, value):
        categories = [item["room_category"] for item in value]
        if len(categories) != len(set(categories)):
            raise serializers.ValidationError("Найдена повторяющиеся категория")
        return value


class PriceCalendarSerializer(serializers.ModelSerializer):
    category_prices = CategoryPriceCalendarSerializer(many=True)

    class Meta:
        model = PriceCalendar
        fields = [
            "id",
            "hotel",
            "start_date",
            "end_date",
            "available_for_booking",
            "discount",
            "discount_amount",
            "category_prices",
        ]
        read_only_fields = ("hotel",)

    def validate(self, data):
        # Проверка дат
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
        # Проверка скидки
        if data.get("discount") and not data.get("discount_amount"):
            raise serializers.ValidationError("Скидка указана, но сумма скидки не указана")
        return data

    def create(self, validated_data):
        categories_data = validated_data.pop("category_prices", [])
        price_calendar = super().create(validated_data)

        # Создаем связанные цены категорий
        category_objs = [
            CategoryPriceCalendar(price_calendar=price_calendar, **cat_data) for cat_data in categories_data
        ]
        CategoryPriceCalendar.objects.bulk_create(category_objs)

        return price_calendar

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("category_prices", [])

        # Обновляем основной объект
        instance = super().update(instance, validated_data)

        # Обновляем связанные объекты
        instance.category_prices.all().delete()
        category_objs = [CategoryPriceCalendar(price_calendar=instance, **cat_data) for cat_data in categories_data]
        CategoryPriceCalendar.objects.bulk_create(category_objs)

        return instance
