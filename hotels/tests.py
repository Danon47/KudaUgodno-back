import base64
from datetime import time
import tempfile
import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (
    Hotel,
    Room,
    RoomAmenity,
    HotelAmenity,
    RoomCategory,
    MealPlan,
)
from .choices import MealChoices, TypeOfHolidayChoices, PlaceChoices


# Создаем временную директорию для MEDIA_ROOT
temp_media_root = tempfile.mkdtemp()


class ModelTestCase(TestCase):
    def setUp(self):
        # Создаём объекты Удобств в отеле, Категорий номеров, Удобств в номере
        self.amenity_hotel = HotelAmenity.objects.create(name="Бассейн")
        self.category = RoomCategory.objects.create(name="Стандарт")
        self.amenity_room = RoomAmenity.objects.create(name="Кондиционер")
        # Создаем объекты типов питания
        self.meal_plans = [
            MealPlan.objects.create(name=MealChoices.NO_MEALS, price_per_person=0),
            MealPlan.objects.create(
                name=MealChoices.ULTRA_ALL_INCLUSIVE, price_per_person=1000
            ),
            MealPlan.objects.create(
                name=MealChoices.ALL_INCLUSIVE, price_per_person=750
            ),
            MealPlan.objects.create(name=MealChoices.FULL_BOARD, price_per_person=500),
            MealPlan.objects.create(name=MealChoices.HALF_BOARD, price_per_person=250),
            MealPlan.objects.create(
                name=MealChoices.ONLY_BREAKFAST, price_per_person=100
            ),
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


@override_settings(MEDIA_ROOT=temp_media_root)
class HotelAPITest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после всех тестов
        shutil.rmtree(temp_media_root)
        super().tearDownClass()

    def setUp(self):
        # Создаем объект Hotel
        self.hotel_data = {
            "name": "Тестовый Отель",
            "star_category": 4,
            "place": PlaceChoices.HOTEL,
            "type_of_holiday": TypeOfHolidayChoices.BEACH,
            "amenities": [{"name": "Бассейн"}, {"name": "Аквапарк"}],
            "country": "Тестовая Страна",
            "city": "Тестовый Город",
            "address": "Тестовый Адрес",
            "distance_to_sea": 1000,
            "distance_to_airport": 5000,
            "description": "Тестовое описание",
            "user_rating": 5.1,
            "check_in_time": time(15, 0),
            "check_out_time": time(11, 0),
        }
        # Кодируем файлы в base64
        self.photo1_base64 = base64.b64encode(b"file_content").decode("utf-8")
        self.photo2_base64 = base64.b64encode(b"file_content").decode("utf-8")
        # Создаем отель
        create_url = reverse("hotels:hotel-list-create")
        create_data = self.hotel_data.copy()
        create_data["photo"] = [
            {"photo": f"data:image/jpeg;base64,{self.photo1_base64}"},
        ]
        response = self.client.post(create_url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Сохраняем ID созданного отеля
        self.hotel_id = response.data["id"]

    def test_hotel_creation(self):
        """Тест проверки создания отеля"""
        hotel = Hotel.objects.get(id=self.hotel_id)
        self.assertEqual(hotel.name, "Тестовый Отель")
        # Проверяем, что фотографии добавлены
        photos = hotel.hotel_photos.all()
        self.assertEqual(photos.count(), 1)

    def test_hotel_update(self):
        """Тест проверки обновления отеля"""
        update_url = reverse("hotels:hotel-detail-update-delete", args=[self.hotel_id])
        # Получаем текущие данные отеля
        hotel = Hotel.objects.get(id=self.hotel_id)

        # Данные для обновления
        update_data = {
            "name": "Обновленный Отель",
            "star_category": 5,
            "photo": [
                {"photo": f"data:image/jpeg;base64,{self.photo2_base64}"},
            ],
            "amenities": [{"name": "Спа"}],  # Обновляем удобства
            # Добавляем обязательные поля с текущими значениями
            "country": hotel.country,
            "city": hotel.city,
            "address": hotel.address,
            "description": hotel.description,
            "user_rating": hotel.user_rating,
        }

        # Отправляем запрос на обновление
        response = self.client.put(update_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что отель обновлен
        updated_hotel = Hotel.objects.get(id=self.hotel_id)
        self.assertEqual(updated_hotel.name, "Обновленный Отель")
        self.assertEqual(updated_hotel.star_category, 5)

        # Проверяем, что фотографии обновлены
        photos = updated_hotel.hotel_photos.all()
        self.assertEqual(photos.count(), 1)
        self.assertTrue(photos[0].photo.name.endswith(".jpg"))

        # Проверяем, что удобства обновлены
        amenities = updated_hotel.amenities.all()
        self.assertEqual(amenities.count(), 1)
        self.assertEqual(amenities[0].name, "Спа")

    def test_hotel_list(self):
        """Тест проверки просмотра списка отелей"""
        # Получаем список отелей
        list_url = reverse("hotels:hotel-list-create")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в списке есть созданный отель
        if "results" in response.data:  # Если используется пагинация
            hotels = response.data["results"]
        else:
            hotels = response.data

        self.assertGreater(len(hotels), 0)  # Проверяем, что список не пуст
        self.assertEqual(hotels[0]["name"], "Тестовый Отель")

    def test_hotel_detail(self):
        """Тест проверки просмотра конкретного отеля"""
        # Запрашиваем данные отеля
        detail_url = reverse("hotels:hotel-detail-update-delete", args=[self.hotel_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные корректны
        self.assertEqual(response.data["name"], "Тестовый Отель")
        self.assertEqual(response.data["star_category"], 4)
        self.assertEqual(len(response.data["photo"]), 1)

    def test_hotel_delete(self):
        """Тест проверки удаления отеля"""
        # Удаляем отель
        delete_url = reverse("hotels:hotel-detail-update-delete", args=[self.hotel_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что отель удален
        with self.assertRaises(Hotel.DoesNotExist):
            Hotel.objects.get(id=self.hotel_id)


@override_settings(MEDIA_ROOT=temp_media_root)
class RoomAPITest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после всех тестов
        shutil.rmtree(temp_media_root)
        super().tearDownClass()

    def setUp(self):
        self.category = RoomCategory.objects.create(name="Стандарт")
        # Создаём объект номер отеля
        self.room_data = {
            "category": self.category.name,
            "meal": [
                {"name": MealChoices.NO_MEALS, "price_per_person": 0},
                {"name": MealChoices.ULTRA_ALL_INCLUSIVE, "price_per_person": 1000},
                {"name": MealChoices.ALL_INCLUSIVE, "price_per_person": 750},
                {"name": MealChoices.FULL_BOARD, "price_per_person": 500},
                {"name": MealChoices.HALF_BOARD, "price_per_person": 250},
                {"name": MealChoices.ONLY_BREAKFAST, "price_per_person": 100},
            ],
            "smoking": False,
            "area": 20,
            "amenities": [
                {"name": "Кондиционер"},
                {"name": "Wi-Fi"},
            ],
            "capacity": 3,
            "single_bed": 1,
            "double_bed": 1,
            "nightly_price": 5000,
            "photo": [{"photo": "photo1.jpg"}],
        }

        # Кодируем файлы в base64
        self.photo1_base64 = base64.b64encode(b"file_content").decode("utf-8")
        self.photo2_base64 = base64.b64encode(b"file_content").decode("utf-8")

        # Создаем номер
        create_url = reverse("hotels:room-list-create")
        create_data = self.room_data.copy()
        create_data["photo"] = [
            {"photo": f"data:image/jpeg;base64,{self.photo1_base64}"}
        ]
        response = self.client.post(create_url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Сохраняем ID созданного номера
        self.room_id = response.data["id"]

    def test_room_creation(self):
        """Тест проверки создания номера"""
        room = Room.objects.get(id=self.room_id)
        self.assertEqual(room.category.name, "Стандарт")
        # Проверяем, что фотографии добавлены
        photos = room.room_photos.all()
        self.assertEqual(photos.count(), 1)

    def test_room_update(self):
        """Тест проверки обновления номера"""
        update_url = reverse("hotels:room-detail-update-delete", args=[self.room_id])

        # Данные для обновления
        update_data = {
            "category": self.category.name,
            "meal": [
                {"name": MealChoices.NO_MEALS, "price_per_person": 0},
                {"name": MealChoices.ULTRA_ALL_INCLUSIVE, "price_per_person": 1000},
                {"name": MealChoices.ALL_INCLUSIVE, "price_per_person": 750},
                {"name": MealChoices.FULL_BOARD, "price_per_person": 500},
                {"name": MealChoices.HALF_BOARD, "price_per_person": 250},
                {"name": MealChoices.ONLY_BREAKFAST, "price_per_person": 100},
            ],
            "smoking": False,  # Обновляем значение
            "area": 40,  # Обновляем значение
            "amenities": [
                {"name": "Кондиционер"},
                {"name": "Wi-Fi"},
            ],
            "capacity": 3,  # Обновляем значение
            "single_bed": 2,  # Обновляем значение
            "double_bed": 1,
            "nightly_price": 150,  # Обновляем значение
            "photo": [{"photo": f"data:image/jpeg;base64,{self.photo2_base64}"}],
        }

        # Отправляем запрос на обновление
        response = self.client.put(update_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что номер обновлен
        updated_room = Room.objects.get(id=self.room_id)
        self.assertEqual(updated_room.smoking, False)
        self.assertEqual(updated_room.area, 40)
        self.assertEqual(updated_room.capacity, 3)
        self.assertEqual(updated_room.single_bed, 2)
        self.assertEqual(updated_room.nightly_price, 150)

        # Проверяем, что фотографии обновлены
        photos = updated_room.room_photos.all()
        self.assertEqual(photos.count(), 1)
        self.assertTrue(photos[0].photo.name.endswith(".jpg"))

    def test_room_list(self):
        """Тест проверки просмотра списка номеров"""
        # Получаем список номеров
        list_url = reverse("hotels:room-list-create")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в списке есть созданный номер
        if "results" in response.data:  # Если используется пагинация
            rooms = response.data["results"]
        else:
            rooms = response.data

        self.assertGreater(len(rooms), 0)  # Проверяем, что список не пуст
        self.assertEqual(rooms[0]["category"], "Стандарт")

    def test_room_detail(self):
        """Тест проверки просмотра конкретного номера"""
        # Запрашиваем данные номера
        detail_url = reverse("hotels:room-detail-update-delete", args=[self.room_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные корректны
        self.assertEqual(response.data["category"], "Стандарт")
        self.assertEqual(response.data["capacity"], 3)
        self.assertEqual(len(response.data["photo"]), 1)

    def test_room_delete(self):
        """Тест проверки удаления номера"""
        # Удаляем номер
        delete_url = reverse("hotels:room-detail-update-delete", args=[self.room_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что номер удален
        with self.assertRaises(Room.DoesNotExist):
            Room.objects.get(id=self.room_id)

    def test_room_amenity_creation(self):
        url = reverse("hotels:room-amenity-create")
        data = {"name": "Фен"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hotel_amenity_creation(self):
        url = reverse("hotels:hotel-amenity-create")
        data = {"name": "Бассейн"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
