from datetime import time
from django.test import TestCase
from hotels.choices import MealChoices, TypeOfHolidayChoices, PlaceChoices
from hotels.models.models_hotel import Hotel
from hotels.models.models_hotel_amenity import HotelAmenity
from hotels.models.models_hotel_meal import MealPlan
from hotels.models.models_room import Room
from hotels.models.models_room_amenity import RoomAmenity
from hotels.models.models_room_caterogy import RoomCategory


class ModelTestCase(TestCase):
    def setUp(self):
        # Создаём объекты Удобств в отеле, Категорий номеров, Удобств в номере
        self.amenity_hotel = HotelAmenity.objects.create(name="Бассейн")
        self.category = RoomCategory.objects.create(name="Стандарт")
        self.amenity_room = RoomAmenity.objects.create(name="Кондиционер")
        # Создаем объекты типов питания
        self.meal_plans = [
            MealPlan.objects.create(name=MealChoices.NO_MEALS, price_per_person=0),
            MealPlan.objects.create(name=MealChoices.ULTRA_ALL_INCLUSIVE, price_per_person=1000),
            MealPlan.objects.create(name=MealChoices.ALL_INCLUSIVE, price_per_person=750),
            MealPlan.objects.create(name=MealChoices.FULL_BOARD, price_per_person=500),
            MealPlan.objects.create(name=MealChoices.HALF_BOARD, price_per_person=250),
            MealPlan.objects.create(name=MealChoices.ONLY_BREAKFAST, price_per_person=100),
        ]
        # Создаём объект отеля
        self.hotel = Hotel.objects.create(
            name="Тестовый Отель",
            star_category=3,
            place=PlaceChoices.HOTEL,
            type_of_holiday=TypeOfHolidayChoices.BEACH,
            country="Тестовая Страна",
            city="Тестовый Город",
            address="Тестовый Адрес",
            distance_to_sea=1000,
            distance_to_airport=5000,
            description="Тестовое описание",
            user_rating=5.1,
            check_in_time=time(15, 0),
            check_out_time=time(11, 0),
        )
        self.hotel.amenities.add(self.amenity_hotel)
        # Создаём объект номера в отеле и связываем его с объектом отеля
        self.hotel_room = Room.objects.create(
            category=self.category,
            smoking=False,
            area=20,
            capacity=3,
            single_bed=1,
            double_bed=1,
            nightly_price=5000,
            hotel=self.hotel,
        )
        self.hotel_room.amenities.add(self.amenity_room)
        self.hotel_room.meal.set(self.meal_plans)

    def test_hotel_creation(self):
        self.assertTrue(isinstance(self.hotel, Hotel))
        self.assertEqual(self.hotel.name, "Тестовый Отель")
        self.assertEqual(self.hotel.place, "Отель")
        self.assertEqual(self.hotel.type_of_holiday, "Пляжный")
        self.assertEqual(self.hotel.amenities.first().name, "Бассейн")
        self.assertEqual(self.hotel.star_category, 3)
        self.assertEqual(self.hotel.country, "Тестовая Страна")
        self.assertEqual(self.hotel.city, "Тестовый Город")
        self.assertEqual(self.hotel.address, "Тестовый Адрес")
        self.assertEqual(self.hotel.distance_to_sea, 1000)
        self.assertEqual(self.hotel.distance_to_airport, 5000)
        self.assertEqual(self.hotel.description, "Тестовое описание")
        self.assertEqual(self.hotel.user_rating, 5.1)
        self.assertEqual(self.hotel.check_in_time, time(15, 0))
        self.assertEqual(self.hotel.check_out_time, time(11, 0))
        # Проверяем, что номер связан с отелем
        self.assertEqual(self.hotel_room.hotel, self.hotel)

    def test_hotel_room_creation(self):
        self.assertTrue(isinstance(self.hotel_room, Room))
        self.assertEqual(self.hotel_room.amenities.first().name, "Кондиционер")
        self.assertEqual(self.hotel_room.category.name, "Стандарт")
        # Проверяем количество типов питания
        self.assertEqual(self.hotel_room.meal.count(), 6)
        # Проверяем каждый тип питания
        for meal_plan in self.meal_plans:
            self.assertIn(meal_plan, self.hotel_room.meal.all())
        self.assertEqual(self.hotel_room.smoking, False)
        self.assertEqual(self.hotel_room.area, 20)
        self.assertEqual(self.hotel_room.capacity, 3)
        self.assertEqual(self.hotel_room.single_bed, 1)
        self.assertEqual(self.hotel_room.double_bed, 1)
        self.assertEqual(self.hotel_room.nightly_price, 5000)
