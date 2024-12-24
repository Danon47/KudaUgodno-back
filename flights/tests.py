from rest_framework import status
from rest_framework.test import APITestCase

from flights.choices import AirlinesChoices
from flights.models import Flight
from django.urls import reverse


class FlightTestCase(APITestCase):
    """
    Тесты для модели Flight
    """

    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="SW 1245",
            airline=AirlinesChoices.AEROFLOT,
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

        url = reverse("flights:flight_detail", args=(self.flight.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("flight_number"), self.flight.flight_number)

    def test_flights_list(self):
        """
        Тест проверки просмотра списка рейсов
        """

        url = reverse("flights:flight_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_flight_create(self):
        """
        Тест проверки создания рейсов
        """

        self.assertEqual(Flight.objects.all().count(), 1)
        self.assertTrue(isinstance(self.flight, Flight))
        self.assertEqual(self.flight.price, 5000)

    def test_flight_update(self):
        """
        Тест проверки изменения рейса
        """
        url = reverse("flights:flight_detail", args=(self.flight.pk,))
        data = {
            "flight_number": "SW 1246",
            "airline": self.flight.airline,  # Сохраните текущее значение или обновите его
            "departure_airport": self.flight.departure_airport,
            "arrival_airport": self.flight.arrival_airport,
            "departure_date": self.flight.departure_date,
            "departure_time": self.flight.departure_time,
            "arrival_date": self.flight.arrival_date,
            "arrival_time": self.flight.arrival_time,
            "price": self.flight.price,
            "service_class": self.flight.service_class,
            "flight_type": self.flight.flight_type,
        }
        response = self.client.patch(url, data, format="json")

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Получаем обновленный объект
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.flight_number, "SW 1246")

    def test_flight_delete(self):
        """
        Тест проверки удаления рейса
        """

        url = reverse("flights:flight_detail", args=(self.flight.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flight.objects.all().count(), 0)
