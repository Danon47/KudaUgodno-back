import pytest
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
        self.assertEqual(hotel.amenities_sports_and_recreation, ["Бассейн", "Тренажёрный зал"])
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
    """ Тест модели правил отеля"""
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
            {"name": "Правило 2", "description": "Описание правила 2"}
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
    def setUp(self):
        self.hotel_data = get_hotel_data()
        self.hotel = Hotel.objects.create(**self.hotel_data)
        self.photo_data = get_hotel_photo_data(self.hotel)
        self.photo = HotelPhoto.objects.create(**self.photo_data)
        self.url_list = reverse("hotels-photos-detail", args=[self.hotel.id])
        self.url_detail = reverse("hotels-photos-detail", args=[self.hotel.id, self.photo.id])

    def test_create_hotel_photo(self):
        """Тест создания фотографии отеля."""
        # Создаём временное изображение, так как если использовать self.photo_data получаю ошибку:
        # {'photo': [ErrorDetail(string='Отправленный файл пуст.', code='empty')]}
        test_image = create_test_image()
        photo_data = {"hotel": self.hotel.id, "photo": test_image,}
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

#
# @pytest.mark.django_db
# class TestHotelEndpoints:
#     def setup_method(self):
#         self.client = APIClient()
#         self.list_url = reverse('hotels-list')
#         self.hotel_data = get_hotel_data()
#         self.hotel_data.pop('check_in_time')  # Время будет передано как строка
#         self.hotel_data.update({
#             "check_in_time": "14:00:00",
#             "check_out_time": "12:00:00",
#             "rules": [{"name": "Тестовое правило", "description": "Описание"}]
#         })
#
#     def test_full_hotel_lifecycle(self):
#         # Создание
#         response = self.client.post(self.list_url, self.hotel_data, format='json')
#         assert response.status_code == status.HTTP_201_CREATED
#         hotel_id = response.data['id']
#
#         # Проверка создания
#         hotel = Hotel.objects.get(id=hotel_id)
#         assert hotel.name == "Тестовый отель"
#         assert hotel.rules.count() == 1
#
#         # Получение списка
#         response = self.client.get(self.list_url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data['results']) == 1
#         assert response.data['results'][0]['room_categories'] == ["Стандарт", "Делюкс"]
#
#         # Детализация
#         detail_url = reverse('hotels-detail', args=[hotel_id])
#         response = self.client.get(detail_url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['type_of_rest'] == "Пляжный"
#
#         # Обновление
#         update_data = {
#             "name": "Обновленное название",
#             "star_category": 4,
#             "rules": [{"name": "Новое правило", "description": "Новое описание"}]
#         }
#         response = self.client.put(detail_url, update_data, format='json')
#         assert response.status_code == status.HTTP_200_OK
#         hotel.refresh_from_db()
#         assert hotel.name == "Обновленное название"
#         assert hotel.rules.first().name == "Новое правило"
#
#         # Удаление
#         response = self.client.delete(detail_url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert Hotel.objects.count() == 0
#
#
# @pytest.mark.django_db
# class TestHotelPhotoEndpoints:
#     def setup_method(self):
#         self.client = APIClient()
#         self.hotel = Hotel.objects.create(**get_hotel_data())
#         self.photo_data = get_hotel_photo_data(self.hotel)
#
#     def test_photo_operations(self):
#         # Создание фото
#         url = reverse('hotels-photos-detail', args=[self.hotel.id])
#         with open(self.photo_data['photo'].name, 'rb') as img:
#             response = self.client.post(url, {'photo': img}, format='multipart')
#
#         assert response.status_code == status.HTTP_201_CREATED
#         photo_id = response.data['id']
#
#         # Проверка создания
#         assert HotelPhoto.objects.count() == 1
#         photo = HotelPhoto.objects.first()
#         assert 'test_image' in photo.photo.name
#
#         # Получение списка фото
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#
#         # Удаление фото
#         delete_url = reverse('hotels-photo-detail', args=[self.hotel.id, photo_id])
#         response = self.client.delete(delete_url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert HotelPhoto.objects.count() == 0
#
#     def test_invalid_photo_upload(self):
#         url = reverse('hotels-photos-detail', args=[self.hotel.id])
#         response = self.client.post(url, {'photo': 'not-an-image'}, format='multipart')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#
#
# @pytest.mark.django_db
# class TestValidation:
#     def test_invalid_star_rating(self):
#         client = APIClient()
#         invalid_data = get_hotel_data().copy()
#         invalid_data['star_category'] = 6
#
#         response = client.post(reverse('hotels-list'), invalid_data, format='json')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert 'star_category' in response.data
