from rest_framework import serializers

from hotels.models.room.date.models_room_date import RoomCategory, RoomDate


class RoomCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий номеров в отеле и их стоимость.
    """

    class Meta:
        model = RoomCategory
        fields = (
            "room",
            "price",
        )


class RoomDateBaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор дат для номеров.
    """

    class Meta:
        model = RoomDate
        fields = (
            "id",
            "start_date",
            "end_date",
            "available_for_booking",
            "stock",
            "share_size",
        )


class RoomDateListSerializer(RoomDateBaseSerializer):
    """
    Сериализатор списка дат для номеров, с деталями по категориям номеров.
    """

    categories = RoomCategorySerializer(many=True)

    class Meta(RoomDateBaseSerializer.Meta):
        fields = RoomDateBaseSerializer.Meta.fields + ("categories",)

    def create(self, validated_data):
        categories_data = validated_data.pop("categories")
        room_date = RoomDate.objects.create(**validated_data)

        # Создание и привязка категорий
        for category_data in categories_data:
            room_category = RoomCategory.objects.create(**category_data)
            room_date.categories.add(room_category)

        return room_date

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("categories", None)

        # Обновляем основные поля
        instance = super().update(instance, validated_data)

        if categories_data is not None:
            # Очищаем старые связи, но не удаляем сами категории
            instance.categories.clear()

            # Добавляем новые категории
            for category_data in categories_data:
                room_category, created = RoomCategory.objects.get_or_create(**category_data)
                instance.categories.add(room_category)

        return instance


class RoomDateDetailSerializer(RoomDateBaseSerializer):
    """
    Детальный сериализатор RoomDate с выводом стоимости конкретного номера.
    Требует передачи номера через context['room'].
    """

    price = serializers.SerializerMethodField()

    class Meta(RoomDateBaseSerializer.Meta):
        fields = RoomDateBaseSerializer.Meta.fields + ("price",)

    def get_price(self, room_date: RoomDate) -> int | None:
        """
        Возвращает стоимость номера на дату.
        Если номер не задан (например, если мы не передаем `room` в контекст сериализатора), то возвращает None.
        """
        room = self.context.get("room")
        try:
            return room_date.categories.get(room=room).price
        except RoomCategory.DoesNotExist:
            return None
