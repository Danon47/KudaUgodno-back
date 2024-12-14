from rest_framework import status
from rest_framework.test import APITestCase

from flights.models import Flight
from django.urls import reverse


class FlightTestCase(APITestCase):

    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="SW-1245",
            airline="Аэрофлот",
            departure_airport="Шереметьево",
            arrival_airport="Адлер",
            departure_date="2024-08-24",
            departure_time="08:00:00",
            arrival_date="2024-08-25",
            arrival_time="12:00:00",
            price=5000,
        )

    def test_flight_retrieve(self):
        """
        Тест проверки просмотра рейса
        """
        url = reverse("flights:flight-detail", args=(self.flight.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("flight_number"), self.flight.flight_number)

    def test_flights_list(self):
        """
        Тест проверки просмотра списка рейсов
        """
        url = reverse("flights:flights-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_flight_create(self):
        """
        Тест проверки создания рейсов
        """
        url = reverse("flights:flight-create")
        data = {
            "flight_number": "VK-1245",
            "airline": "S7",
            "departure_airport": "Шереметьево",
            "arrival_airport": "Адлер",
            "departure_date": "2024-08-24",
            "departure_time": "08:00:00",
            "arrival_date": "2024-08-25",
            "arrival_time": "12:00:00",
            "price": 3000,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.all().count(), 2)

    def test_flight_update(self):
        """
        Тест проверки изменения рейса
        """
        url = reverse("flights:flight-update", args=(self.flight.pk,))
        data = {"airline": "Победа"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("airline"), "Победа")

    def test_flight_delete(self):
        """
        Тест проверки удаления рейса
        """
        url = reverse('flights:flight-delete', args=(self.flight.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Flight.objects.all().count(), 0
        )
