from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import DecimalField, SerializerMethodField
from rest_framework.serializers import ImageField, ModelSerializer

from all_fixture.errors.list_error import TYPE_OF_MEAL_ERROR
from calendars.models import CalendarDate
from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.models import Room, RoomPhoto, RoomRules


class RoomPhotoSerializer(ModelSerializer):
    """
    Сериализатор фотографий номера.
    """

    photo = ImageField()

    class Meta:
        model = RoomPhoto
        fields = (
            "id",
            "photo",
            "room",
        )
        read_only_fields = (
            "id",
            "room",
        )


class RoomRulesSerializer(ModelSerializer):
    """
    Сериализатор правил в номере.
    """

    class Meta:
        model = RoomRules
        fields = (
            "name",
            "option",
        )


class RoomBaseSerializer(ModelSerializer):
    """
    Базовый сериализатор номера.
    """

    rules = RoomRulesSerializer(
        many=True,
    )

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
        extra_kwargs = {
            "type_of_meals": {
                "error_messages": {
                    "does_not_exist": TYPE_OF_MEAL_ERROR,
                    "invalid": "Неверный формат ID типа питания. Ожидается положительное число.",
                    "null": "ID рейса туда не может быть пустым.",
                    "blank": "ID рейса туда не может быть пустым.",
                }
            }
        }

    def create(self, validated_data):
        # Извлекаем данные о правилах и типе питания из валидированных данных
        rules_data = validated_data.pop("rules", [])
        type_of_meals = validated_data.pop("type_of_meals", [])

        # Создаем объект Room
        room = Room.objects.create(**validated_data)

        # Устанавливаем тип питания, если он передан
        if type_of_meals:
            room.type_of_meals.set(type_of_meals)

        # Создаем объекты RoomRules и связываем их с Room
        if rules_data:
            rules = []
            for rule_data in rules_data:
                rule, created = RoomRules.objects.get_or_create(
                    name=rule_data["name"],
                    defaults={
                        "option": rule_data["option"],
                    },
                )
                rules.append(rule)
            room.rules.set(rules)

        return room

    def update(self, instance, validated_data):
        # Извлекаем данные о правилах и типе питания из валидированных данных
        rules_data = validated_data.pop("rules", None)
        type_of_meals = validated_data.pop("type_of_meals", None)

        # Обновляем поля Room
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем тип питания, если он передан
        if type_of_meals is not None:
            instance.type_of_meals.set(type_of_meals)

        # Если в данных есть правила, обновляем их
        if rules_data is not None:
            rules = []
            for rule_data in rules_data:
                rule, created = RoomRules.objects.get_or_create(
                    name=rule_data["name"],
                    defaults={
                        "option": rule_data["option"],
                    },
                )
                rules.append(rule)
            instance.rules.set(rules)

        return instance


class RoomCalendarDateSerializer(ModelSerializer):
    price = SerializerMethodField()
    discount_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default="0.17",
    )

    class Meta:
        model = CalendarDate
        fields = (
            "id",
            "start_date",
            "end_date",
            "available_for_booking",
            "discount",
            "discount_amount",
            "price",
        )

    @extend_schema_field(
        {
            "type": "string",
            "format": "decimal",
            "example": "123.00",
        }
    )
    def get_price(self, obj: CalendarDate) -> str | None:
        room = self.context.get("room")
        if not room:
            return None

        try:
            calendar_price = obj.calendar_prices.get(room=room)
            return str(calendar_price.price)
        except ObjectDoesNotExist:
            return None


class RoomDetailSerializer(RoomBaseSerializer):
    """
    Сериалиазатор для вывода детальной информации о номере.
    """

    calendar_dates = SerializerMethodField(
        read_only=True,
    )
    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )
    type_of_meals = TypeOfMealSerializer(
        many=True,
        read_only=True,
    )
    rules = RoomRulesSerializer(
        many=True,
        read_only=True,
    )
    total_price_without_discount = DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        default="15000.00",
    )
    total_price_with_discount = DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        default="12000.00",
    )

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "photo",
            "calendar_dates",
            "total_price_without_discount",
            "total_price_with_discount",
        )

    @extend_schema_field(field=RoomCalendarDateSerializer(many=True))
    def get_calendar_dates(self, obj: Room):
        request = self.context.get("request")
        start_date_str = request.query_params.get("date_range_after") if request else None
        end_date_str = request.query_params.get("date_range_before") if request else None
        calendar_dates = obj.calendar_dates.all()

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Вычитаем один день из end_date, так как день выезда не учитывается
            adjusted_end_date = end_date - timedelta(days=1)

            calendar_dates = (
                calendar_dates.filter(
                    start_date__lte=adjusted_end_date,
                    end_date__gte=start_date,
                )
                .order_by("start_date")
                .distinct()
            )

        context = self.context.copy()
        context["room"] = obj
        serializer = RoomCalendarDateSerializer(
            calendar_dates,
            many=True,
            context=context,
        )
        return serializer.data
