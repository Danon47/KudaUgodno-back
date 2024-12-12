from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Hotel, HotelRoom, AmenityRoom, AmenityHotel, PlaceHotel
from .choices import *
from datetime import date, timedelta


# class ModelTestCase(TestCase):
#     def setUp(self):
#         self.amenity_room = AmenityRoom.objects.create(name="Кондиционер")
#         self.amenity_hotel = AmenityHotel.objects.create(name="Бассейн")
#         self.place_hotel = PlaceHotel.objects.create(name="Пляжный")
#
#         self.hotel_room = HotelRoom.objects.create(
#             category=CategoryChoices.Standard,
#             food=FoodChoices.Only_breakfast,
#             type_of_holiday=TypeOfHolidayChoices.Beach,
#             smoking=SmokingChoices.Forbidden,
#             pet=PetChoices.Authorized,
#             area=20,
#             capacity=2,
#             bed=BedChoices.Double_1,
#             nightly_price=100,
#             start_date=date.today(),
#             end_date=date.today() + timedelta(days=7),
#         )
#         self.hotel_room.amenities.add(self.amenity_room)
#
#         self.hotel = Hotel.objects.create(
#             name="Тестовый Отель",
#             category=StarsChoices.Three_stars,
#             country="Тестовая Страна",
#             city="Тестовый Город",
#             address="Тестовый Адрес",
#             distance_to_sea=100,
#             distance_to_airport=50,
#             description="Тестовое описание",
#             place=self.place_hotel,
#             check_in_time=time(15, 0),
#             check_out_time=time(11, 0),
#         )
#         self.hotel.amenities.add(self.amenity_hotel)
#         self.hotel.hotel_room.add(self.hotel_room)
#
#     def test_hotel_creation(self):
#         self.assertTrue(isinstance(self.hotel, Hotel))
#         self.assertEqual(self.hotel.__str__(), "Тестовый Отель")
#         self.assertEqual(self.hotel.place.name, "Пляжный")
#         self.assertEqual(self.hotel.amenities.first().name, "Бассейн")
#         self.assertEqual(self.hotel.category, "3 Звезды"),
#         self.assertEqual(self.hotel.country, "Тестовая Страна"),
#         self.assertEqual(self.hotel.city, "Тестовый Город"),
#         self.assertEqual(self.hotel.address, "Тестовый Адрес"),
#         self.assertEqual(self.hotel.distance_to_sea, 100),
#         self.assertEqual(self.hotel.distance_to_airport, 50),
#         self.assertEqual(self.hotel.place.name, "Пляжный"),
#         self.assertEqual(self.hotel.description, "Тестовое описание"),
#         self.assertEqual(self.hotel.check_in_time, time(15, 0)),
#         self.assertEqual(self.hotel.check_out_time, time(11, 0))
#
#
#     def test_hotel_room_creation(self):
#         self.assertTrue(isinstance(self.hotel_room, HotelRoom))
#         self.assertEqual(self.hotel_room.amenities.first().name, "Кондиционер")
#         self.assertEqual(self.hotel_room.category, "Стандарт"),
#         self.assertEqual(self.hotel_room.food, "Только завтраки"),
#         self.assertEqual(self.hotel_room.type_of_holiday, "Пляжный"),
#         self.assertEqual(self.hotel_room.smoking, "Запрещено"),
#         self.assertEqual(self.hotel_room.pet, "Разрешено"),
#         self.assertEqual(self.hotel_room.bed, "1 Двуспальная"),
#         self.assertEqual(self.hotel_room.area, 20),
#         self.assertEqual(self.hotel_room.capacity, 2),
#         self.assertEqual(self.hotel_room.nightly_price, 100),
#         self.assertEqual(self.hotel_room.start_date, date.today()),
#         self.assertEqual(self.hotel_room.end_date, date.today() + timedelta(days=7))


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.amenity_room = AmenityRoom.objects.create(name="Кондиционер")
        self.amenity_hotel = AmenityHotel.objects.create(name="Бассейн")
        self.place_hotel = PlaceHotel.objects.create(name="Пляжный")



    def test_hotel_creations(self):
        """Тест проверки создания отеля"""
        url = reverse("hotels:hotel-list-create")
        data = {
            "name": "Тестовый Отель",
            "category": StarsChoices.Three_stars,
            "country": "Тестовая Страна",
            "city": "Тестовый Город",
            "address": "Тестовый Адрес",
            "distance_to_sea": 100,
            "distance_to_airport": 50,
            "description": "Тестовое описание",
            "place": self.place_hotel.id,
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
            category=StarsChoices.Three_stars,
            country="Тестовая Страна",
            city="Тестовый Город",
            address="Тестовый Адрес",
            distance_to_sea=100,
            distance_to_airport=50,
            description="Тестовое описание",
            place=self.place_hotel,
            check_in_time=time(15, 0),
            check_out_time=time(11, 0),
            # amenities=[self.amenity_hotel.id],
        )
        hotel.amenities.add(self.amenity_hotel)
        url = reverse("hotels:hotel-detail", kwargs={"pk": hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый Отель")

    def test_hotel_room_creation(self):
        """Тест проверки создания номера отеля"""
        url = reverse("hotels:hotel-room-list-create")
        data = {
            "category": CategoryChoices.Standard,
            "food": FoodChoices.Only_breakfast,
            "type_of_holiday": TypeOfHolidayChoices.Beach,
            "smoking": SmokingChoices.Forbidden,
            "pet": PetChoices.Authorized,
            "bed": BedChoices.Double_1,
            "area": 20,
            "amenities": [self.amenity_room.id],
            "capacity": 2,
            "nightly_price": 100,
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

    def test_hotem_room_detail_view(self):
        """Тест проверки получения номера отеля по id"""
        hotel_room = HotelRoom.objects.create(
            category=CategoryChoices.Standard,
            food=FoodChoices.Only_breakfast,
            type_of_holiday=TypeOfHolidayChoices.Beach,
            smoking=SmokingChoices.Forbidden,
            pet=PetChoices.Authorized,
            bed=BedChoices.Double_1,
            area=20,
            capacity=2,
            nightly_price=100,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        hotel_room.amenities.add(self.amenity_room)
        url = reverse("hotels:hotel-room-detail", kwargs={"pk": hotel_room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category"], "Стандарт")

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

    def test_place_hotel_creation(self):
        url = reverse("hotels:place-hotels-list-create")
        data = {"name": "Пляжный"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_place_hotel_list_view(self):
        url = reverse("hotels:place-hotels-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
