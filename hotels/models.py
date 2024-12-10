from django.db import models


NULLABLE = {"blank": True, "null": True}


class Choices:
    """
    Вспомогательный класс для создания choices
    """

    @classmethod
    def pets(cls):
        return [("Authorized", "Разрешено"), ("Forbidden", "Запрещено")]

    @classmethod
    def smoking(cls):
        return [("Authorized", "Разрешено"), ("Forbidden", "Запрещено")]

    @classmethod
    def category(cls):
        return [
            ("Standard", "Стандарт"),
            ("Comfort", "Комфорт"),
            ("Family", "Семейный"),
            ("Lux", "Люкс"),
        ]

    @classmethod
    def food(cls):
        return [
            ("No meals", "Без питания"),
            ("Breakfast included", "Завтрак включён"),
            ("Breakfast and lunch included", "Завтрак и обед включён"),
            ("Breakfast and dinner included", "Завтрак и ужин включён"),
            ("All inclusive", "Всё включено"),
        ]

    @classmethod
    def bed(cls):
        return [
            ("1 Single", "1 Односпальная"),
            ("1 Double", "1 Двуспальная"),
            ("1 Single and 1 Double", "1 Односпальная и 1 Двуспальная"),
            ("2 Singles and 1 Double", "2 Односпальные и 1 Двуспальная"),
            ("2 Singles", "2 Односпальные"),
            ("2 Doubles", "2 Двуспальные"),
            ("2 Singles and 2 Doubles", "2 Односпальные и 2 Двуспальные"),
        ]

    @classmethod
    def stars(cls):
        return [
            ("1 Star", "1 Звезда"),
            ("2 Stars", "2 Звезды"),
            ("3 Stars", "3 Звезды"),
            ("4 Stars", "4 Звезды"),
            ("5 Stars", "5 Звезд"),
        ]

    @classmethod
    def type(cls):
        return [
            ("Hotel", "Отель"),
            ("Hostel", "Хостел"),
            ("Villa", "Вилла"),
            ("Apartments", "Апартаменты"),
            ("Guest house", "Гостевой дом"),
            ("Inn", "Гостиница"),
        ]

    @classmethod
    def in_time(cls):
        return [
            ("14:00", "14:00"),
            ("15:00", "15:00"),
            ("16:00", "16:00"),
            ("17:00", "17:00"),
            ("18:00", "18:00"),
            ("19:00", "19:00"),
            ("20:00", "20:00"),
            ("21:00", "21:00"),
            ("22:00", "22:00"),
            ("23:00", "23:00"),
            ("00:00", "00:00"),
        ]

    @classmethod
    def out_time(cls):
        return [
            ("00:00", "00:00"),
            ("01:00", "01:00"),
            ("02:00", "02:00"),
            ("03:00", "03:00"),
            ("04:00", "04:00"),
            ("05:00", "05:00"),
            ("06:00", "06:00"),
            ("07:00", "07:00"),
            ("08:00", "08:00"),
            ("09:00", "09:00"),
            ("10:00", "10:00"),
            ("11:00", "11:00"),
            ("12:00", "12:00"),
        ]


class HotelRoom(models.Model):
    """
    Класс номера отеля
    """

    # Категория номера
    category = models.CharField(
        max_length=20,
        choices=Choices.category(),
        default="Standard",
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )
    # Тип питания
    food = models.CharField(
        max_length=30,
        choices=Choices.food(),
        default="No meals",
        verbose_name="Тип питания",
        help_text="Выберите тип питания",
    )
    # Курение
    smoking = models.CharField(
        max_length=20,
        choices=Choices.smoking(),
        default="Forbidden",
        verbose_name="Курение",
        help_text="Выберите курение",
    )
    # С животными можно?
    pet = models.CharField(
        max_length=20,
        choices=Choices.pets(),
        default="Forbidden",
        verbose_name="С животными можно?",
        help_text="Выберите с животными можно?",
    )
    # Площадь номера
    area = models.PositiveIntegerField(
        verbose_name="Площадь номера",
        help_text="Введите площадь номера",
    )
    # Количество номеров ?

    # Удобства в номере
    amenities = models.ManyToManyField(
        "AmenityRoom",
        blank=True,
        verbose_name="Удобства в номере",
        help_text="Выберите удобства в номере",
    )
    # Фотографии номера
    image = models.ImageField(
        upload_to="hotels/rooms/",
        verbose_name="Фотография",
        help_text="Загрузите фотографию номера",
    )
    # Количество проживающих людей
    capacity = models.PositiveIntegerField(
        verbose_name="Количество проживающих людей",
        help_text="Введите количество проживающих людей",
    )
    # Кровать
    bed = models.CharField(
        max_length=35,
        choices=Choices.bed(),
        default="1 Single",
        verbose_name="Кровать",
        help_text="Выберите кровать",
    )
    # Стоимость за один день
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        help_text="Введите цену",
    )
    # Ближайшая свободная дата ?

    # Дата начала бронирования
    start_date = models.DateField(
        verbose_name="Дата начала бронирования",
        help_text="Введите дату начала бронирования",
    )
    # Дата окончания бронирования
    end_date = models.DateField(
        verbose_name="Дата окончания бронирования",
        help_text="Введите дату окончания бронирования",
    )

    def __str__(self):
        return f"{self.id} {self.category}"

    class Meta:
        verbose_name = "Класс номера"
        verbose_name_plural = "Классы номеров"
        ordering = ["category"]


class Hotel(models.Model):
    """
    Класс отеля
    """

    # Название отеля
    name = models.CharField(
        max_length=50,
        verbose_name="Название отеля",
        help_text="Введите название отеля",
    )
    # Категория отеля в звёздах
    category = models.CharField(
        max_length=20,
        choices=Choices.stars(),
        default="1 Star",
        verbose_name="Категория отеля",
        help_text="Выберите категорию отеля",
    )
    # Тип размещения
    place = models.CharField(
        max_length=15,
        choices=Choices.type(),
        default="Hotel",
        verbose_name="Тип размещения",
        help_text="Выберите тип размещения",
    )
    # Страна отеля
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
    )
    # Город отеля
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город",
    )
    # Адрес отеля
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес отеля",
        help_text="Введите адрес отеля",
    )
    # Расстояние до моря
    distance_to_sea = models.PositiveIntegerField(
        verbose_name="Расстояние до моря",
        help_text="Введите расстояние до моря",
    )
    # Расстояние до аэропорта
    distance_to_airport = models.PositiveIntegerField(
        verbose_name="Расстояние до аэродрома",
        help_text="Введите расстояние до аэродрома",
    )
    # Описание отеля
    description = models.TextField(
        verbose_name="Описание отеля",
        help_text="Введите описание отеля",
    )
    # Фотографии отеля
    image = models.ImageField(
        upload_to="hotels/",
        verbose_name="Фотография",
        help_text="Загрузите фотографию отеля",
    )
    # Номера в отеле
    hotel_room = models.ForeignKey(
        HotelRoom,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Номера в отеле",
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "AmenityHotel",
        blank=True,
        verbose_name="Удобства в отеле",
        help_text="Выберите удобства в отеле",
    )
    # Пользовательская оценка
    user_rating = models.CharField(
        max_length=255,
        verbose_name="Пользовательская оценка",
        help_text="Введите оценку",
    )
    # Время заселения
    check_in_time = models.TimeField(
        max_length=5,
        choices=Choices.in_time(),
        default="14:00",
        verbose_name="Время заезда",
        help_text="Выберите время заезда",
    )
    # Время выезда
    check_out_time = models.CharField(
        max_length=5,
        choices=Choices.out_time(),
        default="12:00",
        verbose_name="Время выезда",
        help_text="Выберите время выезда",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ["name"]


class AmenityRoom(models.Model):
    """
    Удобства в номере
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
        help_text="Введите удобство",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобство в номере"
        verbose_name_plural = "Удобства в номерах"


class AmenityHotel(models.Model):
    """
    Удобства в отеле
    """

    name = models.CharField(
        max_length=50, verbose_name="Удобство", help_text="Введите удобство"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобство в отеле"
        verbose_name_plural = "Удобства в отеле"
