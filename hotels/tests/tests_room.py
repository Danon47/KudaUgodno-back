import shutil
import tempfile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from hotels.choices import MealChoices
from hotels.models.models_room import Room
from hotels.models.models_room_caterogy import RoomCategory
from hotels.tests.fixtures.temp_image import create_test_image

# Создаем временную директорию для MEDIA_ROOT
temp_media_root = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=temp_media_root)
class RoomAPITest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после всех тестов
        shutil.rmtree(temp_media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.category = RoomCategory.objects.create(name="Стандарт")
        # Используем функцию для создания изображения
        self.photo_file1 = create_test_image()
        self.photo_file2 = create_test_image()

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
        }

        # Создаем номер
        create_url = reverse("hotels:room-list-create")
        create_data = self.room_data.copy()
        response = self.client.post(create_url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Сохраняем ID созданного номера
        self.room_id = response.data["id"]

        # Добавляем фотографию к номеру
        photo_upload_url = reverse(
            "hotels:room-photo-create", kwargs={"room_pk": self.room_id}
        )
        photo_data = {"photo": self.photo_file1}
        response = self.client.post(photo_upload_url, photo_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Добавляем вторую фотограцию к номеру
        photo_upload_url = reverse(
            "hotels:room-photo-create", kwargs={"room_pk": self.room_id}
        )
        photo_data = {"photo": self.photo_file2}
        response = self.client.post(photo_upload_url, photo_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_room_creation(self):
        """Тест проверки создания номера"""
        room = Room.objects.get(id=self.room_id)
        self.assertEqual(room.category.name, "Стандарт")
        # Проверяем, что фотографии добавлены
        photos = room.room_photos.all()
        self.assertEqual(photos.count(), 2)

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
            "nightly_price": 3500,  # Обновляем значение
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
        self.assertEqual(updated_room.nightly_price, 3500)

    def test_room_list(self):
        """Тест проверки просмотра списка номеров"""
        # Получаем список номеров
        list_url = reverse("hotels:room-list-create")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в списке есть созданный номер
        if "results" in response.data:
            rooms = response.data["results"]
        else:
            rooms = response.data

        self.assertGreater(len(rooms), 0)
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
        self.assertEqual(len(response.data["photo"]), 2)

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
