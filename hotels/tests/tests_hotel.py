from datetime import time
import shutil
import tempfile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from hotels.choices import PlaceChoices, TypeOfHolidayChoices
from hotels.models.models_hotel import Hotel
from hotels.tests.fixtures.temp_image import create_test_image

# Создаем временную директорию для MEDIA_ROOT
temp_media_root = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=temp_media_root)
class HotelAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после всех тестов
        shutil.rmtree(temp_media_root)
        super().tearDownClass()

    # --- Новая группа: Тест CRUD для отеля ---
    def test_hotel_crud(self):
        """CRUD тест для отеля"""
        # Создаем объект Hotel
        hotel_data = {
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

        # Создание отеля
        create_url = reverse("hotels:hotel-list-create")
        response = self.client.post(create_url, hotel_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Сохраняем ID созданного отеля
        self.hotel_id = response.data.get("id", None)
        # Убедитесь, что отель был создан и ID сохранен
        if not self.hotel_id:
            raise ValueError("Ошибка создания отеля, ID отсутствует.")
        print(f"Response data from hotel creation: {response.data}")

        # Обновление отеля
        update_url = reverse("hotels:hotel-detail-update-delete", args=[self.hotel_id])
        print("Update URL:", update_url)
        print("Hotel ID:", self.hotel_id)

        update_data = hotel_data.copy()
        update_data["name"] = "Обновленный Отель"
        response = self.client.put(update_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Обновленный Отель")

        # Удаление отеля
        delete_url = reverse("hotels:hotel-detail-update-delete", args=[self.hotel_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что отель удален
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # --- Существующая группа: Тесты списка и деталей отеля ---
    def test_hotel_list(self):
        """Тест проверки списка отелей"""
        list_url = reverse("hotels:hotel-list-create")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_hotel_detail(self):
        """Тест проверки деталей отеля"""
        # Создаем объект Hotel
        hotel_data = {
            "name": "Тестовый Отель",
            "star_category": 4,
            "place": PlaceChoices.HOTEL,
            "type_of_holiday": TypeOfHolidayChoices.BEACH,
            "country": "Тестовая Страна",
            "city": "Тестовый Город",
            "address": "Тестовый Адрес",
            "description": "Тестовое описание",
            "user_rating": 5.1,
            "check_in_time": "15:00:00",
            "check_out_time": "11:00:00",
        }

        # Создаем отель
        create_url = reverse("hotels:hotel-list-create")
        response = self.client.post(create_url, hotel_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Сохраняем ID отеля
        hotel_id = response.data["id"]
        # Проверяем детали отеля
        detail_url = reverse("hotels:hotel-detail-update-delete", args=[hotel_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый Отель")


    # --- Существующая группа: Тесты с удобствами ---
    def test_hotel_amenity_creation(self):
        """Тест добавления удобств"""
        # Создаем отель
        hotel_data = {
            "name": "Тестовый Отель",
            "star_category": 4,
            "place": PlaceChoices.HOTEL,
            "type_of_holiday": TypeOfHolidayChoices.BEACH,
            "country": "Тестовая Страна",
            "city": "Тестовый Город",
            "address": "Тестовый Адрес",
            "description": "Тестовое описание",
            "user_rating": 5.1,
        }
        create_url = reverse("hotels:hotel-list-create")
        response = self.client.post(create_url, hotel_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Добавляем удобства
        hotel_id = response.data["id"]
        amenity_url = reverse("hotels:hotel-amenity-create", args=[hotel_id])
        amenity_data = {"name": "Бассейн"}
        response = self.client.post(amenity_url, amenity_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
