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

# Отображение ошибки
decimal_ivalid = {"invalid": "Введите цену с точкой, а не с запятой."}


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
    name="type_of_meal_id",
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
