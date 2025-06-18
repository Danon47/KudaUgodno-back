from rest_framework.serializers import ImageField, ModelSerializer, SerializerMethodField

from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.models import Room, RoomCategory, RoomDate, RoomPhoto, RoomRules


class RoomPhotoSerializer(ModelSerializer):
    """
    Сериализатор фотографий номера.
    """

    photo = ImageField()

    class Meta:
        model = RoomPhoto
        fields = ("id", "photo", "room")
        read_only_fields = ("id", "room")


class RoomRulesSerializer(ModelSerializer):
    """
    Сериализатор правил в номере.
    """

    class Meta:
        model = RoomRules
        fields = ("name", "option")


class RoomBaseSerializer(ModelSerializer):
    """
    Базовый сериализатор номера.
    """

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "type_of_meals",
            "number_of_adults",
            "number_of_children",
            "single_bed",
            "double_bed",
            "area",
            "quantity_rooms",
            "amenities_common",
            "amenities_coffee",
            "amenities_bathroom",
            "amenities_view",
            "rules",
        )


class RoomDateBaseSerializer(ModelSerializer):
    """
    Сериализатор дат для номеров.
    """

    class Meta:
        model = RoomDate
        fields = ("id", "start_date", "end_date", "available_for_booking", "discount", "discount_amount")


class RoomDateDetailSerializer(RoomDateBaseSerializer):
    """
    Детальный сериализатор RoomDate с выводом стоимости конкретного номера.
    Требует передачи номера через context['room'].
    """

    price = SerializerMethodField()

    class Meta(RoomDateBaseSerializer.Meta):
        fields = RoomDateBaseSerializer.Meta.fields + ("price",)

    def get_price(self, room_date: Room) -> int | None:
        """
        Возвращает стоимость номера на дату.
        Если номер не задан (например, если мы не передаем `room` в контекст сериализатора), то возвращает None.
        """
        room = self.context.get(
            "room",
        )
        try:
            return room_date.categories.get(room=room).price
        except RoomCategory.DoesNotExist:
            return None


class RoomDetailSerializer(RoomBaseSerializer):
    """
    Сериалиазатор для вывода детальной информации о номере.
    """

    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )
    dates = SerializerMethodField()
    type_of_meals = TypeOfMealSerializer(many=True)
    rules = RoomRulesSerializer(many=True)

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + ("dates", "photo")

    def get_dates(self, obj: RoomDate) -> list:
        """
        Получает список объектов RoomDate связанных с номером.
        Этот метод фильтрует объекты RoomDate, связанные с указанным номером, по его категориям, обеспечивая
        уникальность и упорядочивая их по дате начала.
        Затем он сериализует список с помощью RoomDateSerializer.
        Аргументы:
            obj (Room): Экземпляр номера, для которого извлекаются даты.
        Returns:
            list: Список сериализованных объектов RoomDate.
        """
        room_dates = (
            RoomDate.objects.filter(categories__room=obj)
            .distinct()
            .order_by("start_date")
            .prefetch_related("categories")
        )
        return RoomDateDetailSerializer(room_dates, many=True, context={"room": obj}).data


class RoomCategorySerializer(ModelSerializer):
    """
    Сериализатор категорий номеров в отеле и их стоимость.
    """

    class Meta:
        model = RoomCategory
        fields = ("room", "price")


class RoomDateListSerializer(RoomDateBaseSerializer):
    """
    Сериализатор списка дат для номеров, с деталями по категориям номеров.
    """

    categories = RoomCategorySerializer(many=True)

    class Meta(RoomDateBaseSerializer.Meta):
        fields = RoomDateBaseSerializer.Meta.fields + ("categories",)

    def create(self, validated_data):
        categories_data = validated_data.pop(
            "categories",
        )
        room_date = RoomDate.objects.create(**validated_data)

        # Создание и привязка категорий
        for category_data in categories_data:
            room_category = RoomCategory.objects.get_or_create(**category_data)
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
