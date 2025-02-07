from drf_spectacular.utils import OpenApiParameter, OpenApiExample


# Теги для settings
user_settings = {
    "name": "Пользователи",
    "description": "Методы для работы с пользователями"
}
tour_settings = {
    "name": "Туры",
    "description": "Методы для работы с турами"
}
hotel_settings = {
    "name": "Отель",
    "description": "Методы для работы с отелями"
}
hotel_amenity_common_settings = {
    "name": "Удобства общие в отеле",
    "description": "Методы для работы с общими удобствами отелей",
}
hotel_amenity_room_settings = {
    "name": "Удобства в номере в отеле",
    "description": "Методы для работы с удобствами в номерах отелей",
}
hotel_amenity_sport_settings = {
    "name": "Удобства спорт и отдых в отеле",
    "description": "Методы для работы с удобствами спорта и отдыха",
}
hotel_amenity_children_settings = {
    "name": "Удобства для детей в отеле",
    "description": "Методы для работы с удобствами для детей",
}
hotel_rules_settings = {
    "name": "Правила в отеле",
    "description": "Методы для работы с правилами отелей",
}
hotel_photo_settings = {
    "name": "Фотографии в отеле",
    "description": "Методы для работы с фотографиями отелей",
}
room_settings = {
    "name": "Номер",
    "description": "Методы для работы с номерами"
}
room_category_settings = {
    "name": "Категории номера",
    "description": "Методы для работы с категориями номеров",
}
room_amenity_settings = {
    "name": "Удобства в номере",
    "description": "Методы для работы с удобствами номеров",
}
room_photo_settings = {
    "name": "Фотографии номера",
    "description": "Методы для работы с фотографиями номеров",
}
flight_settings = {
    "name": "Рейсы",
    "description": "Методы для работы с рейсами"
}
application_settings = {
    "name": "Заявки",
    "description": "Методы для работы с заявками"
}
application_guest_settings = {
    "name": "Гости",
    "description": "Методы для работы с гостями"
}

# ID пользователя
user_id = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Пользователя",
    required=True,
)
# ID тура
tour_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Тура",
    required=True,
)
# ID отеля
hotel_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="hotel_id",
    type=int,
    description="ID Отеля",
    required=False,
)
# ID номера
room_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="room_id",
    type=int,
    description="ID Номера",
    required=False,
)
# ID фотографии в номере
room_id_photo = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Фотографии номера",
    required=True,
)
# ID фотографии в отеле
hotel_id_photo = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Фотографий отеля",
    required=True,
)
# ID в отеле
id_hotel = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Отеля",
    required=False,
)
# ID номера
id_room = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Номера",
    required=True,
)
# ID удобства
id_room_amenity = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Удобств",
    required=True,
)
# ID категории номера
id_room_category = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Категории номера",
    required=True,
)
# ID тура
flight_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Рейса",
    required=True,
)
# ID заявки
application_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Заявки",
    required=True,
)
# ID гостя
application_guest_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Гостя в заявке",
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
