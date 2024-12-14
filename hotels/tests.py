from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Hotel, HotelRoom, AmenityRoom, AmenityHotel, CategoryHotelRoom
from .choices import *
from datetime import date, timedelta


class ModelTestCase(TestCase):
    def setUp(self):
        self.amenity_room = AmenityRoom.objects.create(name="Кондиционер")
        self.category = CategoryHotelRoom.objects.create(name="Стандарт")
        self.amenity_hotel = AmenityHotel.objects.create(name="Бассейн")

        self.hotel_room = HotelRoom.objects.create(
            category=self.category,
            food=FoodChoices.ONLY_BREAKFAST,
            type_of_holiday=TypeOfHolidayChoices.BEACH,
            smoking=False,
            pet=False,
            area=20,
            capacity=2,
            single_bed=1,
            double_bed=1,
            nightly_price=6500,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        self.hotel_room.amenities.add(self.amenity_room)

        self.hotel = Hotel.objects.create(
            name="Тестовый Отель",
            star_category=3,
            place=PlaceChoices.HOTEL,
            country="Тестовая Страна",
            city="Тестовый Город",
            address="Тестовый Адрес",
            distance_to_sea=100,
            distance_to_airport=50,
            description="Тестовое описание",
            user_rating=5.1,
            check_in_time=time(15, 0),
            check_out_time=time(11, 0),
        )
        self.hotel.amenities.add(self.amenity_hotel)
        self.hotel.hotel_room.add(self.hotel_room)

    def test_hotel_creation(self):
        self.assertTrue(isinstance(self.hotel, Hotel))
        self.assertEqual(self.hotel.__str__(), "Тестовый Отель")
        self.assertEqual(self.hotel.place, "Отель")
        self.assertEqual(self.hotel.amenities.first().name, "Бассейн")
        self.assertEqual(self.hotel.star_category, 3)
        self.assertEqual(self.hotel.country, "Тестовая Страна")
        self.assertEqual(self.hotel.city, "Тестовый Город")
        self.assertEqual(self.hotel.address, "Тестовый Адрес")
        self.assertEqual(self.hotel.distance_to_sea, 100)
        self.assertEqual(self.hotel.distance_to_airport, 50)
        self.assertEqual(self.hotel.description, "Тестовое описание")
        self.assertEqual(self.hotel.user_rating, 5.1)
        self.assertEqual(self.hotel.check_in_time, time(15, 0))
        self.assertEqual(self.hotel.check_out_time, time(11, 0))

    def test_hotel_room_creation(self):
        self.assertTrue(isinstance(self.hotel_room, HotelRoom))
        self.assertEqual(self.hotel_room.amenities.first().name, "Кондиционер")
        self.assertEqual(self.hotel_room.category.name, "Стандарт")
        self.assertEqual(self.hotel_room.food, "Только завтраки")
        self.assertEqual(self.hotel_room.type_of_holiday, "Пляжный")
        self.assertEqual(self.hotel_room.smoking, False)
        self.assertEqual(self.hotel_room.pet, False)
        self.assertEqual(self.hotel_room.single_bed, 1)
        self.assertEqual(self.hotel_room.double_bed, 1)
        self.assertEqual(self.hotel_room.area, 20)
        self.assertEqual(self.hotel_room.capacity, 2)
        self.assertEqual(self.hotel_room.nightly_price, 6500)
        self.assertEqual(self.hotel_room.start_date, date.today())
        self.assertEqual(self.hotel_room.end_date, date.today() + timedelta(days=7))


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.amenity_room = AmenityRoom.objects.create(name="Кондиционер")
        self.category = CategoryHotelRoom.objects.create(name="Стандарт")
        self.amenity_hotel = AmenityHotel.objects.create(name="Бассейн")

    def test_hotel_room_creation(self):
        """Тест проверки создания номера отеля"""
        url = reverse("hotels:hotel-room-list-create")
        data = {
            "category": self.category.id,
            "food": FoodChoices.ONLY_BREAKFAST,
            "type_of_holiday": TypeOfHolidayChoices.BEACH,
            "smoking": False,
            "pet": False,
            "single_bed": 1,
            "double_bed": 1,
            "area": 20,
            "amenities": [self.amenity_room.id],
            "capacity": 2,
            "nightly_price": 6500,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=7),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hotel_room_list_view(self):
        """Тест проверки получения списка номеров отеля"""
        url = reverse("hotels:hotel-room-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_hotel_room_detail_view(self):
        """Тест проверки получения номера отеля по id"""
        hotel_room = HotelRoom.objects.create(
            category=self.category,
            food=FoodChoices.ONLY_BREAKFAST,
            type_of_holiday=TypeOfHolidayChoices.BEACH,
            smoking=False,
            pet=False,
            single_bed=1,
            double_bed=1,
            area=20,
            capacity=2,
            nightly_price=6500,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        hotel_room.amenities.add(self.amenity_room)
        url = reverse("hotels:hotel-room-detail", kwargs={"pk": hotel_room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hotel_creations(self):
        """Тест проверки создания отеля"""
        url = reverse("hotels:hotel-list-create")
        data = {
            "name": "Тестовый Отель",
            "star_category": 3,
            "country": "Тестовая Страна",
            "city": "Тестовый Город",
            "address": "Тестовый Адрес",
            "distance_to_sea": 100,
            "distance_to_airport": 50,
            "description": "Тестовое описание",
            "place": "Отель",
            "user_rating": 5.1,
            "check_in_time": time(15, 0),
            "check_out_time": time(11, 0),
            "amenities": [self.amenity_hotel.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hotel_list_view(self):
        """Тест проверки получения списка отелей"""
        url = reverse("hotels:hotel-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_hotel_detail_view(self):
        """Тест проверки получения отеля по id"""
        hotel = Hotel.objects.create(
            name="Тестовый Отель",
            star_category=3,
            country="Тестовая Страна",
            city="Тестовый Город",
            address="Тестовый Адрес",
            distance_to_sea=100,
            distance_to_airport=50,
            description="Тестовое описание",
            place="Отель",
            user_rating=5.1,
            check_in_time=time(15, 0),
            check_out_time=time(11, 0),
        )
        hotel.amenities.add(self.amenity_hotel)
        url = reverse("hotels:hotel-detail", kwargs={"pk": hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый Отель")

    def test_amenity_room_creation(self):
        url = reverse("hotels:amenity-room-list-create")
        data = {"name": "Фен"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_amenity_room_list_view(self):
        url = reverse("hotels:amenity-room-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_amenity_hotel_creation(self):
        url = reverse("hotels:amenity-hotel-list-create")
        data = {"name": "Бассейн"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_amenity_hotel_list_view(self):
        url = reverse("hotels:amenity-hotel-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
