from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from all_fixture.errors.list_error import (
    DATE_ERROR,
    DECIMAL_ERROR,
    FLIGHT_ERROR,
    HOTEL_ID_ERROR,
    MAILING_EMAIL_ERROR,
    MAILING_ID_ERROR,
    MIN_ERROR,
    PHOTO_ERROR,
    ROOM_ID_ERROR,
    TOUR_MAX_PRICE_ERROR,
    TOUR_STOCK_DISCOUNT_MAX_ERROR,
    TOUR_STOCK_DISCOUNT_MIN_ERROR,
    TOUROPERATOR_ERROR,
    TYPE_OF_MEAL_ERROR,
)
from all_fixture.errors.serializers_error import (
    MailingErrorSerializer,
    RoomBaseEroorSerializer,
    RoomDateErrorBaseSerializer,
    TourErrorBaseSerializer,
    TourStockErrorBaseSerializer,
)

MAILING_400 = OpenApiResponse(
    response=MailingErrorSerializer,
    description="Ошибка валидации",
    examples=[
        OpenApiExample(
            name="Ошибка: Email уже есть в БД",
            value={"email": [MAILING_EMAIL_ERROR]},
            response_only=True,
        )
    ],
)
MAILING_404 = OpenApiResponse(
    response=MailingErrorSerializer,
    description="Рассылка не найдена",
    examples=[
        OpenApiExample(
            name="Ошибка: Рассылка не найдена",
            value={"detail": MAILING_ID_ERROR},
            response_only=True,
        )
    ],
)

TOUR_CREATE_400 = OpenApiResponse(
    response=TourErrorBaseSerializer,
    description="Ошибки при создании тура",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Неправильный формат даты начала тура",
            value={"start_date": DATE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Неправильный формат даты окончания тура",
            value={"end_date": DATE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейс вылета не найден",
            value={"flight_to": FLIGHT_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейс прилета не найден",
            value={"flight_from": FLIGHT_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Туроператор не найден",
            value={"tour_operator": TOUROPERATOR_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Отель не найден",
            value={"hotel": HOTEL_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер не найден",
            value={"rooms": ROOM_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Тип питания не найден",
            value={"type_of_meals": TYPE_OF_MEAL_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейтинг не может быть меньше 0.0",
            value={"price": MIN_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейтинг не может быть меньше 99999999.0",
            value={"price": TOUR_MAX_PRICE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Ввода стоимости",
            value={"price": DECIMAL_ERROR},
        ),
    ],
)

TOUR_UPDATE_400 = OpenApiResponse(
    response=TourErrorBaseSerializer,
    description="Ошибки при обновлении тура",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Неправильный формат даты начала тура",
            value={"start_date": DATE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Неправильный формат даты окончания тура",
            value={"end_date": DATE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейс вылета не найден",
            value={"flight_to": FLIGHT_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейс прилета не найден",
            value={"flight_from": FLIGHT_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Туроператор не найден",
            value={"tour_operator": TOUROPERATOR_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Отель не найден",
            value={"hotel": HOTEL_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер не найден",
            value={"rooms": ROOM_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Тип питания не найден",
            value={"type_of_meals": TYPE_OF_MEAL_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейтинг не может быть меньше 0.0",
            value={"price": MIN_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Рейтинг не может быть меньше 99999999.0",
            value={"price": TOUR_MAX_PRICE_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Ввода стоимости",
            value={"price": DECIMAL_ERROR},
        ),
    ],
)


TOUR_STOCK_400 = OpenApiResponse(
    response=TourStockErrorBaseSerializer,
    description="Ошибки валидации",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Размер скидки меньше чем 0.01",
            value={"discount_amount": TOUR_STOCK_DISCOUNT_MIN_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Размер скидки больше чем 99999.99",
            value={"discount_amount": TOUR_STOCK_DISCOUNT_MAX_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Не правильный формат даты",
            value={"end_date": DATE_ERROR},
        ),
    ],
)

ROOM_CREATE_400 = OpenApiResponse(
    response=RoomBaseEroorSerializer,
    description="Ошибка при создании номера в отеле",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Тип питания из отеля не найден",
            value={"type_of_meals": TYPE_OF_MEAL_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Некорректный тип питания",
            value={"type_of_meals": "Некорректный тип. Ожидалось значение первичного ключа, получен str."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во взрослых не может быть больше 10",
            value={"number_of_adults": "Убедитесь, что это значение меньше либо равно 10."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во взрослых не может быть меньше 1",
            value={"number_of_adults": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во взрослых",
            value={"number_of_adults": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во детей не может быть больше 10",
            value={"number_of_children": "Убедитесь, что это значение меньше либо равно 10."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во детей не может быть меньше 1",
            value={"number_of_children": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во детей",
            value={"number_of_children": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во односпальных кроватей не может быть больше 5",
            value={"single_bed": "Убедитесь, что это значение меньше либо равно 5."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во односпальных кроватей не может быть меньше 1",
            value={"single_bed": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число односпальных кроватей",
            value={"single_bed": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во двуспальных кроватей не может быть больше 3",
            value={"double_bed": "Убедитесь, что это значение меньше либо равно 3."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во двуспальных кроватей не может быть меньше 1",
            value={"double_bed": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число двуспальных кроватей",
            value={"double_bed": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Площадь комнаты не может быть больше 1000",
            value={"area": "Убедитесь, что это значение меньше либо равно 1000."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Площадь комнаты не может быть меньше 1",
            value={"area": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число площади комнаты",
            value={"area": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во комнат не может быть больше 500",
            value={"quantity_rooms": "Убедитесь, что это значение меньше либо равно 500."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во комнат не может быть меньше 1",
            value={"quantity_rooms": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во комнат",
            value={"quantity_rooms": "Введите правильное число."},
        ),
    ],
)

ROOM_UPDATE_400 = OpenApiResponse(
    response=RoomBaseEroorSerializer,
    description="Ошибка при обновлении номера в отеле",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Тип питания из отеля не найден",
            value={"type_of_meals": TYPE_OF_MEAL_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Некорректный тип питания",
            value={"type_of_meals": "Некорректный тип. Ожидалось значение первичного ключа, получен str."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во взрослых не может быть больше 10",
            value={"number_of_adults": "Убедитесь, что это значение меньше либо равно 10."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во взрослых не может быть меньше 1",
            value={"number_of_adults": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во взрослых",
            value={"number_of_adults": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во детей не может быть больше 10",
            value={"number_of_children": "Убедитесь, что это значение меньше либо равно 10."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во детей не может быть меньше 1",
            value={"number_of_children": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во детей",
            value={"number_of_children": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во односпальных кроватей не может быть больше 5",
            value={"single_bed": "Убедитесь, что это значение меньше либо равно 5."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во односпальных кроватей не может быть меньше 1",
            value={"single_bed": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число односпальных кроватей",
            value={"single_bed": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во двуспальных кроватей не может быть больше 3",
            value={"double_bed": "Убедитесь, что это значение меньше либо равно 3."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во двуспальных кроватей не может быть меньше 1",
            value={"double_bed": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число двуспальных кроватей",
            value={"double_bed": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Площадь комнаты не может быть больше 1000",
            value={"area": "Убедитесь, что это значение меньше либо равно 1000."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Площадь комнаты не может быть меньше 1",
            value={"area": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число площади комнаты",
            value={"area": "Введите правильное число."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во комнат не может быть больше 500",
            value={"quantity_rooms": "Убедитесь, что это значение меньше либо равно 500."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Кол-во комнат не может быть меньше 1",
            value={"quantity_rooms": "Убедитесь, что это значение больше либо равно 1."},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Введено не целое число кол-во комнат",
            value={"quantity_rooms": "Введите правильное число."},
        ),
    ],
)

ROOM_RETRIEVE_404 = OpenApiResponse(
    response=RoomDateErrorBaseSerializer,
    description="Ошибки при получении информации о номера в отеле",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Отель не найден",
            value={"detail": HOTEL_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер в отеле не найден",
            value={"detail": ROOM_ID_ERROR},
        ),
    ],
)
ROOM_UPDATE_404 = OpenApiResponse(
    response=RoomDateErrorBaseSerializer,
    description="Ошибки при обновлении информации о номера в отеле",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Отель не найден",
            value={"detail": HOTEL_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер в отеле не найден",
            value={"detail": ROOM_ID_ERROR},
        ),
    ],
)
ROOM_DESTROY_404 = OpenApiResponse(
    response=RoomDateErrorBaseSerializer,
    description="Ошибки при удалении номера в отеле",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Отель не найден",
            value={"detail": HOTEL_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер в отеле не найден",
            value={"detail": ROOM_ID_ERROR},
        ),
    ],
)
ROOM_PHOTO_CREATE_404 = OpenApiResponse(
    response=RoomBaseEroorSerializer,
    description="Ошибки при создании фотографии в номере",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер не найден",
            value={"detail": ROOM_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Фотография в номере не найдена",
            value={"detail": PHOTO_ERROR},
        ),
    ],
)
ROOM_PHOTO_DESTROY_404 = OpenApiResponse(
    response=RoomBaseEroorSerializer,
    description="Ошибки при удалении фотографии в номере",
    examples=[
        OpenApiExample(
            response_only=True,
            name="Ошибка: Номер не найден",
            value={"detail": ROOM_ID_ERROR},
        ),
        OpenApiExample(
            response_only=True,
            name="Ошибка: Фотография в номере не найдена",
            value={"detail": PHOTO_ERROR},
        ),
    ],
)
