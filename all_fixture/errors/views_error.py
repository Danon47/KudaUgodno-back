from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from all_fixture.errors.list_error import (
    DATE_ERROR,
    DECIMAL_ERROR,
    FLIGHT_ERROR,
    HOTEL_ID_ERROR,
    MAILING_EMAIL_ERROR,
    MAILING_ID_ERROR,
    MIN_ERROR,
    ROOM_ID_ERROR,
    TOUR_MAX_PRICE_ERROR,
    TOUR_STOCK_DISCOUNT_MAX_ERROR,
    TOUR_STOCK_DISCOUNT_MIN_ERROR,
    TOUROPERATOR_ERROR,
    TYPE_OF_MEAL_ERROR,
)
from all_fixture.errors.serializers_error import (
    MailingErrorSerializer,
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
