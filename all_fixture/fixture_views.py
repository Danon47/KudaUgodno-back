from drf_spectacular.utils import OpenApiParameter


NULLABLE = {"blank": True, "null": True}
# Теги для settings
user_settings = {"name": "Пользователи", "description": "Методы для работы с пользователями"}
entreprise = {"name": "Компании", "description": "Методы для работы с компаниями"}
auth = {"name": "Авторизация", "description": "Методы для работы с авторизацией"}
tour_settings = {"name": "Туры", "description": "Методы для работы с турами"}
hotel_settings = {"name": "Отели", "description": "Методы для работы с отелями"}
hotel_photo_settings = {
    "name": "Фотографии в отеле",
    "description": "Методы для работы с фотографиями отелей",
}
room_settings = {"name": "Номера", "description": "Методы для работы с номерами"}
room_photo_settings = {
    "name": "Фотографии номера",
    "description": "Методы для работы с фотографиями номеров",
}
flight_settings = {"name": "Рейсы", "description": "Методы для работы с рейсами"}
application_settings = {"name": "Заявки", "description": "Методы для работы с заявками"}
application_guest_settings = {"name": "Гости", "description": "Методы для работы с гостями"}
insurance_settings = {"name": "Страховки", "description": "Методы для работы со страховками"}

# ID пользователя
user_id = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Пользователя",
    required=True,
)
# ID компании
entreprise_id = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Компании",
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
# ID Рейса
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
# ID страховки
insurance_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Страховки",
    required=True,
)

# Для пагинации
limit = OpenApiParameter(
    name="limit",
    type=int,
    description="Количество объектов на одной странице",
    required=False,
)
offset = OpenApiParameter(
    name="offset",
    type=int,
    description="Начальный индекс для пагинации",
    required=False,
)
