from rest_framework import status
from rest_framework.test import APITestCase

from hotels.choices import TypeOfHolidayChoices
from hotels.models import Room, RoomCategory
from tours.choices import FoodChoices
from tours.models import Tour
from django.urls import reverse


class TourTestCase(APITestCase):
    """
    Тесты для модели Tour.
    """

    def setUp(self):
        self.tour = Tour.objects.create(
            start_date="2024-08-24", end_date="2024-08-25", departure_city="Москва"
        )

    def test_tour_retrieve(self):
        """
        Тест проверки просмотра тура
        """
        url = reverse("tours:tour_detail", args=(self.tour.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("start_date"), self.tour.start_date)

    def test_tours_list(self):
        """
        Тест проверки просмотра списка туров
        """
        url = reverse("tours:tour_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tour_create(self):
        """
        Тест проверки создания тура
        """

        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertTrue(isinstance(self.tour, Tour))
        self.assertEqual(self.tour.departure_city, "Москва")

    def test_tour_update(self):
        """
        Тест проверки изменения тура
        """
        url = reverse("tours:tour_detail", args=(self.tour.pk,))
        data = {"name": "Тест"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тест")

    def test_tour_delete(self):
        """
        Тест проверки удаления тура
        """
        url = reverse("tours:tour_detail", args=(self.tour.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tour.objects.all().count(), 0)
