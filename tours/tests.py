from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import Tour
from django.urls import reverse


class TourTestCase(APITestCase):
    """
    Тесты для модели Tour.
    """

    def setUp(self):
        self.tour = Tour.objects.create(
            start_date="2028-08-24", end_date="2028-08-25", departure_city="Москва"
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
        data = {
            "start_date": "2029-09-01",
            "end_date": "2029-09-05",
            "departure_city": "Санкт-Петербург",
            "guests_number": 3,
            "food": "ONLY_BREAKFAST",
            "price": 12000,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tour.refresh_from_db()
        self.assertEqual(self.tour.start_date, date(2029, 9, 1))
        self.assertEqual(self.tour.end_date, date(2029, 9, 5))
        self.assertEqual(self.tour.departure_city, "Санкт-Петербург")
        self.assertEqual(self.tour.guests_number, 3)

    def test_tour_delete(self):
        """
        Тест проверки удаления тура
        """
        url = reverse("tours:tour_detail", args=(self.tour.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tour.objects.all().count(), 0)
