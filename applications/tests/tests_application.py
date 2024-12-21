from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from applications.models import Application, Guest
from hotels.models import Hotel, Room, RoomCategory
from tours.models import Tour
from users.models import User


class ApplicationTest(TestCase):
    """
    Тесты для модели Application
    """

    def setUp(self):
        """
        Экземпляр модели Заявка
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user")
        self.category = RoomCategory.objects.create(name="Стандарт")
        self.hotel = Hotel.objects.create(
            name="Тест Отель",
            star_category=5,
            country="Россия",
            city="Москва",
            address="Пушкина",
            description="Тест описание",
        )
        self.room = Room.objects.create(
            area=20,
            category=self.category,
            capacity=2,
            nightly_price=10000,
            hotel=self.hotel,
        )
        self.tour = Tour.objects.create(
            name="Тур Тест",
            start_date="2024-08-24",
            end_date="2024-08-25",
        )
        self.guest = Guest.objects.create(
            firstname="Иван",
            lastname="Иванов",
            date_born="1999-09-09",
            citizenship="Россия",
        )
        self.application = Application.objects.create(
            tour=self.tour,
            email="test@test.ru",
            phone_number="+7(999)999-99-99",
            visa=1,
            med_insurance=True,
            cancellation_insurance=True,
            wishes="test wishes",
            status="Подтвержден",
            user_owner=self.user,
        )
        self.application.quantity_rooms.add(self.room)
        self.application.quantity_guests.add(self.guest)

    def test_application(self):
        """
        Тест модели Заявки
        """

        self.assertEqual(self.application.tour, self.tour),
        self.assertEqual(self.application.email, "test@test.ru"),
        self.assertEqual(self.application.phone_number, "+7(999)999-99-99"),
        self.assertEqual(self.application.visa, 1),
        self.assertEqual(self.application.med_insurance, True),
        self.assertEqual(self.application.cancellation_insurance, True),
        self.assertEqual(self.application.wishes, "test wishes"),
        self.assertEqual(self.application.status, "Подтвержден"),
        self.assertEqual(self.application.user_owner, self.user)

    def test_application_list(self):
        """Тест на вывод списка заявок"""
        url = reverse("applications:application_list_create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_applications_create(self):
        """Тест создания заявки"""

        url = reverse("applications:application_list_create")

        data = {
            "tour": self.tour.id,
            "email": "user@example.com",
            "phone_number": "+79999999999",
            "quantity_rooms": [self.room.id],
            "quantity_guests": [self.guest.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 2)

    def test_application_retrieve(self):
        """Тест на вывод конкретной заявки"""

        url = reverse(
            "applications:application_detail_update_delete", args=(self.application.pk,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["email"], "test@test.ru")

    def test_applications_put(self):
        """Тест на обновление заявки"""

        url = reverse("applications:application_detail_update_delete", args=(self.application.pk,))
        data = {
            "pk": 6,
            "tour": self.tour.pk,
            "email": "test1@test.ru",
            "phone_number": "+79999999988",
            "visa": 1,
            "med_insurance": False,
            "cancellation_insurance": False,
            "wishes": "test wishes new",
            "status": "Подтвержден",
            "user_owner": self.user.pk,
            "quantity_rooms": [self.room.pk],
            "quantity_guests": [self.guest.pk]
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["wishes"], "test wishes new")

    def test_application_patch(self):
        """Тест на частичное обновление заявки"""

        url = reverse("applications:application_detail_update_delete", args=(self.application.pk,))
        data = {
            "email": "test2@test.ru",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["email"], "test2@test.ru")

    def test_applications_delete(self):
        """Удаление заявки"""

        url = reverse("applications:application_detail_update_delete", args=(self.application.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)
