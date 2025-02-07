from drf_spectacular.utils import OpenApiParameter, OpenApiExample


# Теги для settings
tags_user_settings = {
    "name": "Пользователи",
    "description": "Методы для работы с пользователями"
}
tags_tour_settings = {
    "name": "Туры",
    "description": "Методы для работы с турами"
}
tags_hotel_settings = {
    "name": "Отель",
    "description": "Методы для работы с отелями"
}
tags_hotel_amenity_common_settings = {
    "name": "Удобства общие в отеле",
    "description": "Методы для работы с общими удобствами отелей",
}
tags_hotel_amenity_room_settings = {
    "name": "Удобства в номере в отеле",
    "description": "Методы для работы с удобствами в номерах отелей",
}
tags_hotel_amenity_sport_settings = {
    "name": "Удобства спорт и отдых в отеле",
    "description": "Методы для работы с удобствами спорта и отдыха",
}
tags_hotel_amenity_children_settings = {
    "name": "Удобства для детей в отеле",
    "description": "Методы для работы с удобствами для детей",
}
tags_hotel_rules_settings = {
    "name": "Правила в отеле",
    "description": "Методы для работы с правилами отелей",
}
tags_hotel_photo_settings = {
    "name": "Фотографии в отеле",
    "description": "Методы для работы с фотографиями отелей",
}
tags_room_settings = {
    "name": "Номер",
    "description": "Методы для работы с номерами"
}
tags_room_category_settings = {
    "name": "Категории номера",
    "description": "Методы для работы с категориями номеров",
}
tags_room_amenity_settings = {
    "name": "Удобства в номере",
    "description": "Методы для работы с удобствами номеров",
}
tags_room_photo_settings = {
    "name": "Фотографии номера",
    "description": "Методы для работы с фотографиями номеров",
}
tags_flight_settings = {
    "name": "Рейсы",
    "description": "Методы для работы с рейсами"
}
tags_application_settings = {
    "name": "Заявки",
    "description": "Методы для работы с заявками"
}
tags_application_guest_settings = {
    "name": "Гости",
    "description": "Методы для работы с гостями"
}

# ID пользователя
user_id = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID пользователя",
    required=True,
)
# ID тура
tour_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID тура",
    required=True,
)
# ID отеля
hotel_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="hotel_id",
    type=int,
    description="ID отеля",
    required=False,
)
# ID номера
room_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="room_id",
    type=int,
    description="ID номера",
    required=False,
)
# ID фотографии в номере
room_id_photo = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID фотографии номера",
    required=True,
)
# ID фотографии в отеле
hotel_id_photo = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID фотографий отеля",
    required=True,
)
# ID в отеле
id_hotel = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID отеля",
    required=False,
)
# ID номера
id_room = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID номера",
    required=True,
)
# ID удобства
id_room_amenity = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID удобства",
    required=True,
)
# ID категории номера
id_room_category = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID категории номера",
    required=True,
)
# ID тура
flight_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID тура",
    required=True,
)

# Для пагинации
limit = OpenApiParameter(
    name="limit",
    type=int,
    description="Количество номеров для возврата на страницу",
    required=False,
    examples=[
        OpenApiExample("Пример 1", value=10),
        OpenApiExample("Пример 2", value=20),
    ],
)
offset = OpenApiParameter(
    name="offset",
    type=int,
    description="Начальный индекс для пагинации",
    required=False,
)
