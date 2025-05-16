from rest_framework import serializers

from hotels.models.room.date.models_room_date import RoomCategory, RoomDate


class RoomCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий номеров в отеле и их стоимость.
    """

    class Meta:
        model = RoomCategory
        fields = ("price",)


class RoomCategoryIdSerializer(RoomCategorySerializer):
    """
    Сериализация для того, чтобы к стоимости добавить номер
    """

    class Meta(RoomCategorySerializer.Meta):
        fields = ("room",) + RoomCategorySerializer.Meta.fields


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

    categories = RoomCategoryIdSerializer(many=True)

    class Meta(RoomDateBaseSerializer.Meta):
        fields = RoomDateBaseSerializer.Meta.fields + ("categories",)


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
        if not room:
            return None
        try:
            return room_date.categories.get(room=room).price
        except RoomCategory.DoesNotExist:
            return None
