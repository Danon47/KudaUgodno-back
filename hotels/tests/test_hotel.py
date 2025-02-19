import os
import shutil
import tempfile

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from all_fixture.tests.fixture_hotel import (
    get_hotel_data,
    get_hotel_photo_data,
    get_hotel_rules_data,
)
from all_fixture.tests.test_temp_image import create_test_image
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules


class HotelModelTest(TestCase):
    """Тест модели отеля"""

    def test_hotel_creation(self):
        hotel_data = get_hotel_data()
        hotel = Hotel.objects.create(**hotel_data)

        self.assertEqual(hotel.name, "Тестовый отель")
        self.assertEqual(hotel.star_category, 5)
        self.assertEqual(hotel.place, "Отель")
        self.assertEqual(hotel.country, "Россия")
        self.assertEqual(hotel.city, "Москва")
        self.assertEqual(hotel.address, "ул. Пушкина, д. 1")
        self.assertEqual(hotel.distance_to_the_station, 3500)
        self.assertEqual(hotel.distance_to_the_sea, 20000)
        self.assertEqual(hotel.distance_to_the_center, 2000)
        self.assertEqual(hotel.distance_to_the_metro, 1500)
        self.assertEqual(hotel.distance_to_the_airport, 3000)
        self.assertEqual(hotel.description, "Тестовое описание")
        self.assertEqual(hotel.check_in_time.strftime("%H:%M:%S"), "14:00:00")
        self.assertEqual(hotel.check_out_time.strftime("%H:%M:%S"), "12:00:00")
        self.assertEqual(hotel.amenities_common, ["Wi-Fi", "Парковка"])
        self.assertEqual(hotel.amenities_in_the_room, ["ТВ", "Мини-бар"])
        self.assertEqual(
            hotel.amenities_sports_and_recreation, ["Бассейн", "Тренажёрный зал"]
        )
        self.assertEqual(hotel.amenities_for_children, ["Детская площадка"])
        self.assertEqual(hotel.type_of_meals_ultra_all_inclusive, 5000)
        self.assertEqual(hotel.type_of_meals_all_inclusive, 4000)
        self.assertEqual(hotel.type_of_meals_full_board, 3000)
        self.assertEqual(hotel.type_of_meals_half_board, 2000)
        self.assertEqual(hotel.type_of_meals_only_breakfast, 1000)
        self.assertEqual(hotel.user_rating, 8.5)
        self.assertEqual(hotel.type_of_rest, "Пляжный")
        self.assertEqual(hotel.is_active, True)
        self.assertEqual(hotel.room_categories, ["Стандарт", "Делюкс"])


class HotelPhotoModelTest(TestCase):
    """Тест модели фотографий отеля"""

    def test_hotel_photo_creation(self):
        hotel_data = get_hotel_data()
        hotel = Hotel.objects.create(**hotel_data)
        photo_data = get_hotel_photo_data(hotel)
        photo = HotelPhoto.objects.create(**photo_data)
        self.assertEqual(photo.hotel, hotel)
        self.assertIsNotNone(photo.photo)
        self.assertTrue(photo.photo.name.startswith("hotels/hotels/"))


class HotelRulesModelTest(TestCase):
    """Тест модели правил отеля"""

    def test_hotel_rules_creation(self):
        hotel_data = get_hotel_data()
        hotel = Hotel.objects.create(**hotel_data)
        rules_data = get_hotel_rules_data(hotel)
        rule = HotelRules.objects.create(**rules_data)
        self.assertEqual(rule.hotel, hotel)
        self.assertEqual(rule.name, "Тестовое название правила")
        self.assertEqual(rule.description, "Тестовое описание правила")


class HotelAPITestCase(APITestCase):
    def setUp(self):
        self.hotel_data = get_hotel_data()
        self.hotel_rules_data = get_hotel_rules_data(self.hotel_data)
        self.hotel = Hotel.objects.create(**self.hotel_data)
        self.url_list = reverse("hotels-list")
        self.url_detail = reverse("hotels-detail", args=[self.hotel.id])

    def test_create_hotel(self):
        """Тест создания отеля."""
        response = self.client.post(self.url_list, self.hotel_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 2)

    def test_get_hotel_list(self):
        """Тест получения списка отелей."""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_hotel_detail(self):
        """Тест получения деталей отеля."""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hotel_data["name"])

    def test_update_hotel(self):
        """Тест обновления отеля."""
        updated_data = self.hotel_data.copy()
        updated_data["name"] = "Обновлённое название отеля"
        updated_data["rules"] = [
            {"name": "Правило 1", "description": "Описание правила 1"},
            {"name": "Правило 2", "description": "Описание правила 2"},
        ]
        response = self.client.put(self.url_detail, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Обновлённое название отеля")

    def test_delete_hotel(self):
        """Тест удаления отеля."""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hotel.objects.count(), 0)


class HotelPhotoAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём временную директорию для MEDIA_ROOT
        cls.temp_media_root = tempfile.mkdtemp(prefix="test_media_")
        settings.MEDIA_ROOT = cls.temp_media_root

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после завершения всех тестов
        shutil.rmtree(cls.temp_media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.hotel_data = get_hotel_data()
        self.hotel = Hotel.objects.create(**self.hotel_data)
        self.photo_data = get_hotel_photo_data(self.hotel)
        self.photo = HotelPhoto.objects.create(**self.photo_data)
        self.url_list = reverse("hotels-photos-detail", args=[self.hotel.id])
        self.url_detail = reverse(
            "hotels-photos-detail", args=[self.hotel.id, self.photo.id]
        )

    def test_create_hotel_photo(self):
        """Тест создания фотографии отеля."""
        # Создаём временное изображение, так как если использовать self.photo_data получаю ошибку:
        # {'photo': [ErrorDetail(string='Отправленный файл пуст.', code='empty')]}
        test_image = create_test_image()
        photo_data = {
            "hotel": self.hotel.id,
            "photo": test_image,
        }
        response = self.client.post(self.url_list, photo_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HotelPhoto.objects.count(), 2)

    def test_get_hotel_photo_list(self):
        """Тест получения списка фотографий отеля."""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_hotel_photo(self):
        """Тест удаления фотографии отеля."""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HotelPhoto.objects.count(), 0)
