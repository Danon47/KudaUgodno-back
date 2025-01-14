from datetime import time
import shutil
import tempfile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from hotels.choices import PlaceChoices, TypeOfHolidayChoices
from hotels.models.models_hotel import Hotel

# Создаем временную директорию для MEDIA_ROOT
temp_media_root = tempfile.mkdtemp()


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

        # Создаем отель
        create_url = reverse("hotels:hotel-list-create")
        create_data = self.hotel_data.copy()
        response = self.client.post(create_url, create_data)
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
            # Обязательные поля с текущими значениями
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

    def test_hotel_amenity_creation(self):
        url = reverse("hotels:hotel-amenity-create")
        data = {"name": "Бассейн"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)