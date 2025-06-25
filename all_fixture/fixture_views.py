from drf_spectacular.utils import OpenApiParameter


NULLABLE = {"blank": True, "null": True}
# Теги для settings
user_settings = {"name": "Пользователи", "description": "Методы для работы с пользователями"}
entreprise = {"name": "Компании", "description": "Методы для работы с компаниями"}
auth = {"name": "Авторизация", "description": "Методы для работы с авторизацией"}
tour_settings = {"name": "Туры", "description": "Методы для работы с турами"}
tour_stock_settings = {"name": "Акции в туре", "description": "Методы для работы с акциями в туре"}
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
what_about_settings = {"name": "Что на счёт ...", "description": "Получаем список подборок что насчёт..."}
type_of_meal_settings = {"name": "Тип питания", "description": "Методы для работы с типами питания"}
room_date_settings = {
    "name": "Даты доступности номеров",
    "description": "Методы для работы с датами доступности номеров",
}
MAILING_SETTINGS = {"name": "Рассылки", "description": "Методы для работы с рассылками"}

# Отображение ошибки
decimal_ivalid = {"invalid": "Введите цену с точкой, а не с запятой."}

# Сеттинг Вжухи
vzhuh_settings = {
    "name": "Вжухи",
    "description": "Список актуальных спецпредложений по направлениям",
}

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
# ID акции тура
tour_stock_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Акции тура",
    required=True,
)
# Город вылета(Обязательный)
tour_departure_city = OpenApiParameter(
    name="departure_city",
    type=str,
    description="Город вылета",
    required=True,
)
# Город прилета(Обязательный)
tour_arrival_city = OpenApiParameter(
    name="arrival_city",
    type=str,
    description="Город прилета",
    required=True,
)
# Дата вылета(Обязательный)
tour_start_date = OpenApiParameter(
    name="start_date",
    type=str,
    description="Дата начала тура",
    required=True,
)
# Количество ночей в туре(Обязательный)
tour_nights = OpenApiParameter(
    name="nights",
    type=int,
    description="Количество ночей",
    required=True,
)
# Количество гостей в туре(Обязательный)
tour_guests = OpenApiParameter(
    name="guests",
    type=int,
    description="Количество гостей",
    required=True,
)
# Город вылета(Необязательный)
tour_departure_city_optional = OpenApiParameter(
    name="departure_city",
    type=str,
    description="Город вылета",
    required=False,
)
# Город прилета(Необязательный)
tour_arrival_city_optional = OpenApiParameter(
    name="arrival_city",
    type=str,
    description="Город прилета",
    required=False,
)
# Дата вылета(Необязательный)
tour_start_date_optional = OpenApiParameter(
    name="start_date", description="Дата начала тура", required=False, type=str
)
# Количество нрочей в туре(Необязательный)
tour_nights_optional = OpenApiParameter(name="nights", type=int, description="Количество ночей", required=False)
# Количество гостей в туре(Необязательный)
tour_guests_optional = OpenApiParameter(name="guests", type=int, description="Количество гостей", required=False)
# Город отеля
filter_city = OpenApiParameter(name="city", type=str, description="Город отеля", required=False)
# Тип размещения
filter_place = OpenApiParameter(
    name="place",
    type=str,
    description="Тип размещения",
    required=False,
)
# Тип отдыха
filter_type_of_rest = OpenApiParameter(name="type_of_rest", type=str, description="Тип отдыха", required=False)
# Пользовательская оценка
filter_user_rating = OpenApiParameter(
    name="user_rating", type=float, description="Пользовательская оценка", required=False
)
# Расстояние от отеля до аэропорта
filter_distance_to_the_airport = OpenApiParameter(
    name="distance_to_the_airport", type=int, description="Расстояние до аэропорта в метрах", required=False
)
# Максимальная стоимость тура
tour_price_lte = OpenApiParameter(
    name="price_lte",
    type=int,
    description="Максимальная стоимость тура",
    required=False,
)
# Минимальная стоимость тура
tour_price_gte = OpenApiParameter(
    name="price_gte",
    type=int,
    description="Минимальная стоимость тура",
    required=False,
)
# Туроператор
filter_tour_operator = OpenApiParameter(
    name="tour_operator",
    type=str,
    description="Туроператор",
    required=False,
)
# Категория отеля в кол-ве звед
filter_star_category = OpenApiParameter(
    name="star_category",
    type=str,
    description="Категорию отеля (от 0 до 5)",
    required=False,
)
# ID отеля
hotel_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="hotel_id",
    type=int,
    description="ID Отеля",
    required=False,
)
# ID типа питания
type_of_meal_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID типа питания",
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
# Дата заезда в отель(Обязательный)
hotel_check_in = OpenApiParameter(
    name="check_in_date", description="Дата заезда (YYYY-MM-DD)", required=True, type=str
)
# Дата выезда из отеля(Обязательный)
hotel_check_out = OpenApiParameter(
    name="check_out_date", description="Дата выезда (YYYY-MM-DD)", required=True, type=str
)
# Количество гостей в отеле(Обязательный)
hotel_guests = OpenApiParameter(name="guests", description="Количество гостей", required=True, type=int)
# Название отеля
hotel_city = OpenApiParameter(
    name="hotel_city",
    type=str,
    description="Название города",
    required=False,
)
# Дата заезда в отель(Необязательный)
hotel_check_in_optional = OpenApiParameter(
    name="check_in_date", description="Дата заезда (YYYY-MM-DD)", required=False, type=str
)
# Дата выезда из отеля(Необязательный)
hotel_check_out_optional = OpenApiParameter(
    name="check_out_date", description="Дата выезда (YYYY-MM-DD)", required=False, type=str
)
# Количество гостей в отеле(Необязательный)
hotel_guests_optional = OpenApiParameter(name="guests", description="Количество гостей", required=False, type=int)
# Максимальная стоимость отеля
hotel_price_lte = OpenApiParameter(
    name="price_lte",
    type=int,
    description="Максимальная стоимость отеля",
    required=False,
)
# Минимальная стоимость отеля
hotel_price_gte = OpenApiParameter(
    name="price_gte",
    type=int,
    description="Минимальная стоимость отеля",
    required=False,
)

# ID Даты стоимости номеров
room_date_id = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Даты стоимости номеров",
    required=True,
)
# ID рассылки
MAILING_ID = OpenApiParameter(
    location=OpenApiParameter.PATH,
    name="id",
    type=int,
    description="ID Рассылки",
    required=True,
)
# Рейс страна вылета
flight_departure_country = OpenApiParameter(
    name="departure_country",
    type=str,
    description="Страна вылета",
    required=False,
)
# Рейс город вылета
flight_departure_city = OpenApiParameter(
    name="departure_city",
    type=str,
    description="Город вылета",
    required=False,
)
# Рейс дата вылета
flight_departure_date = OpenApiParameter(
    name="departure_date",
    type=str,
    description="Дата вылета",
    required=False,
)
# Рейс страна вылета
flight_arrival_country = OpenApiParameter(
    name="arrival_country",
    type=str,
    description="Страна прилёта",
    required=False,
)
# Рейс город вылета
flight_arrival_city = OpenApiParameter(
    name="arrival_city",
    type=str,
    description="Город прилёта",
    required=False,
)
# Рейс дата вылета
flight_arrival_date = OpenApiParameter(
    name="arrival_date",
    type=str,
    description="Дата прилёта",
    required=False,
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

WARM_COUNTRIES = [
    "Египет",
    "Египет",
    "Марокко",
    "Тунис",
    "ЮАР",
    "Сейшельские острова",
    "Маврикий",
    "Кения",
    "Танзания",
    "Таиланд",
    "Мальдивы",
    "Индонезия",
    "Филиппины",
    "Вьетнам",
    "Малайзия",
    "Шри-Ланка",
    "ОАЭ",
    "Израиль",
    "Индия",
    "Испания",
    "Греция",
    "Италия",
    "Португалия",
    "Хорватия",
    "Турция",
    "Кипр",
    "Мальта",
    "Мексика",
    "Ямайка",
    "Доминиканская Республика",
    "Багамы",
    "Куба",
    "Коста-Рика",
    "Бразилия",
    "Аргентина",
    "Уругвай",
    "Колумбия",
    "Эквадор",
    "Австралия",
    "Фиджи",
    "Папуа-Новая Гвинея",
    "Самоа",
    "Тонга",
]

WARM_CITY = [
    # Африка
    "Шарм-эль-Шейх",
    "Хургада",
    "Александрия",
    "Марса-Алам",  # Египет
    "Агадир",
    "Эс-Сувейра",
    "Танжер",  # Марокко
    "Сусс",
    "Хаммамет",
    "Джерба",
    "Монастир",  # Тунис
    "Кейптаун",
    "Дурбан",  # ЮАР
    "Виктория",  # Сейшельские острова
    "Порт-Луи",  # Маврикий
    "Момбаса",
    "Малинди",  # Кения
    "Занзибар",
    "Дар-эс-Салам",  # Танзания
    # Азия
    "Пхукет",
    "Паттайя",
    "Самуи",
    "Краби",  # Таиланд
    "Мале",  # Мальдивы
    "Бали",
    "Ломбок",
    "Джакарта",  # Индонезия
    "Манила",
    "Себу",
    "Палаван",  # Филиппины
    "Нячанг",
    "Фантьет",
    "Да Нанг",
    "Хойан",  # Вьетнам
    "Куала-Лумпур",
    "Пенанг",
    "Лангкави",  # Малайзия
    "Коломбо",
    "Галле",
    "Тринкомали",  # Шри-Ланка
    "Дубай",
    "Абу-Даби",
    "Рас-эль-Хайма",  # ОАЭ
    "Тель-Авив",
    "Эйлат",  # Израиль
    "Панаджи",
    "Мумбаи",
    "Кочин",  # Индия
    # Европа
    "Барселона",
    "Малага",
    "Ибица",
    "Тенерифе",  # Испания
    "Афины",
    "Санторини",
    "Родос",
    "Крит",  # Греция
    "Неаполь",
    "Палермо",
    "Кальяри",
    "Римини",  # Италия
    "Лиссабон",
    "Алгарве",  # Португалия
    "Дубровник",
    "Сплит",
    "Пула",  # Хорватия
    "Анталья",
    "Аланья",
    "Бодрум",
    "Измир",
    "Сиде",  # Турция
    "Лимассол",
    "Пафос",  # Кипр
    "Валлетта",
    "Слима",  # Мальта
    # Карибский бассейн и Центральная Америка
    "Канкун",
    "Пуэрто-Вальярта",
    "Акапулько",
    "Тулум",  # Мексика
    "Монтего-Бей",
    "Оча-Риос",  # Ямайка
    "Пунта-Кана",
    "Ла-Романа",  # Доминиканская Республика
    "Нассау",  # Багамы
    "Варадеро",
    "Гавана",  # Куба
    "Сан-Хосе",
    "Тамариндо",  # Коста-Рика
    # Южная Америка
    "Рио-де-Жанейро",
    "Сан-Паулу",
    "Форталеза",
    "Натал",  # Бразилия
    "Мар-дель-Плата",  # Аргентина
    "Пунта-дель-Эсте",  # Уругвай
    "Картахена",
    "Санта-Марта",  # Колумбия
    "Гуаякиль",  # Эквадор
    # Океания
    "Сидней",
    "Голд-Кост",  # Австралия
    "Сува",  # Фиджи
    "Порт-Морсби",  # Папуа-Новая Гвинея
    "Апиа",  # Самоа
    "Нукуалофа",  # Тонга
]
