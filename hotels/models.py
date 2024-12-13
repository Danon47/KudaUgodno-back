from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *


NULLABLE = {"blank": True, "null": True}


class HotelRoom(models.Model):
    """
    Класс номера отеля
    """

    # Категория номера
    category = models.ForeignKey(
        "CategoryHotelRoom",
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )
    # Тип питания
    food = models.CharField(
        max_length=30,
        choices=FoodChoices.choices,
        default=FoodChoices.ONLY_BREAKFAST,
        verbose_name="Тип питания",
        help_text="Выберите тип питания",
    )
    # Тип отдыха
    type_of_holiday = models.CharField(
        max_length=15,
        choices=TypeOfHolidayChoices.choices,
        default=TypeOfHolidayChoices.BEACH,
        verbose_name="Тип отдыха",
        help_text="Выберите тип отдыха",
    )
    # Курение
    smoking = models.BooleanField(
        default=False,
        verbose_name="Курение разрешено?",
        help_text="Да/Нет",
    )
    # С животными можно?
    pet = models.BooleanField(
        default=False,
        verbose_name="С животными разрешено?",
        help_text="Да/Нет",
    )
    # Площадь номера
    area = models.PositiveIntegerField(
        verbose_name="Площадь номера",
        help_text="Введите площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
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
        **NULLABLE,
    )
    # Количество проживающих людей
    capacity = models.PositiveIntegerField(
        verbose_name="Количество проживающих людей",
        help_text="Введите количество проживающих людей",
    )
    # Односпальная кровать
    single_bed = models.IntegerField(
        verbose_name="Односпальная кровать",
        help_text="Выберите кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Двуспальная кровать
    double_bed = models.IntegerField(
        verbose_name="Двуспальная кровать",
        help_text="Выберите кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Цена за ночь
    nightly_price = models.PositiveIntegerField(
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
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["category"]


class Hotel(models.Model):
    """
    Класс отеля
    """

    # Название отеля
    hotel_name = models.CharField(
        max_length=100,
        verbose_name="Название отеля",
        help_text="Введите название отеля",
    )
    # Категория отеля в звёздах
    star_category = models.IntegerField(
        verbose_name="Категория отеля",
        help_text="Выберите категорию отеля (от 0 до 5)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        default=0,
    )
    # Тип размещения
    place = models.ForeignKey(
        "PlaceHotel",
        related_name="hotels",
        on_delete=models.CASCADE,
        verbose_name="Тип размещения",
        help_text="Выберите тип размещения",
        null=True,
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
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Расстояние до аэропорта
    distance_to_airport = models.PositiveIntegerField(
        verbose_name="Расстояние до аэродрома",
        help_text="Введите расстояние до аэродрома",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
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
        **NULLABLE,
    )
    # Номера в отеле
    hotel_room = models.ManyToManyField(
        HotelRoom,
        related_name="rooms",
        verbose_name="Номера в отеле",
        blank=True,
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "AmenityHotel",
        blank=True,
        verbose_name="Удобства в отеле",
        help_text="Выберите удобства в отеле",
    )
    # Пользовательская оценка
    user_rating = models.PositiveIntegerField(
        verbose_name="Пользовательская оценка",
        help_text="Введите оценку",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        **NULLABLE,
    )
    # Время заселения
    check_in_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.in_time(),
        default=time(14, 0),
        verbose_name="Время заезда",
        help_text="Выберите время заезда",
    )
    # Время выезда
    check_out_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.out_time(),
        default=time(12, 0),
        verbose_name="Время выезда",
        help_text="Выберите время выезда",
    )

    def __str__(self):
        return self.hotel_name

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ["hotel_name"]


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
        max_length=50,
        verbose_name="Удобство",
        help_text="Введите удобство",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобство в отеле"
        verbose_name_plural = "Удобства в отеле"


class PlaceHotel(models.Model):
    """
    Тип размещения
    """

    name = models.CharField(
        max_length=15,
        verbose_name="Тип размещения",
        help_text="Выберите тип размещения",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип размещения"
        verbose_name_plural = "Типы размещения"
        ordering = ["name"]


class CategoryHotelRoom(models.Model):
    """
    Категория номера
    """

    name = models.CharField(
        max_length=20,
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"
