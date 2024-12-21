from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from applications.models import Guest
from users.models import User


class GuestTest(TestCase):
    """Тест для модели Гость"""

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create(username="test_user")
        self.guest = Guest.objects.create(
            firstname="Ivan",
            lastname="Ivanov",
            surname="Ivanovich",
            date_born="2000-12-12",
            citizenship="Россия",
            russian_passport_no="1234 567890",
            international_passport_no="12 3456789",
            validity_international_passport="2024-11-11",
        )
        self.guest.user_owner.add(self.user)

    def test_guest(self):
        """Тест модели Гость"""

        self.assertEqual(self.guest.firstname, "Ivan")
        self.assertEqual(self.guest.lastname, "Ivanov")
        self.assertEqual(self.guest.surname, "Ivanovich")
        self.assertEqual(self.guest.date_born, "2000-12-12")
        self.assertEqual(self.guest.citizenship, "Россия")
        self.assertEqual(self.guest.russian_passport_no, "1234 567890")
        self.assertEqual(self.guest.international_passport_no, "12 3456789")
        self.assertEqual(self.guest.validity_international_passport, "2024-11-11")
        self.assertEqual(self.guest.user_owner.count(), 1)

    def test_guest_list(self):
        """Тест на вывод списка гостей"""

        url = reverse("applications:guest_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_guest_retrieve(self):
        """Тест на вывод конкретного заказа"""

        url = reverse("applications:guest_detail_update_delete", args=(self.guest.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["firstname"], "Ivan")

    def test_guest_put(self):
        """Тест на изменение заявки"""

        url = reverse("applications:guest_detail_update_delete", args=(self.guest.pk,))
        data = {
            "firstname": "Sasha",
            "lastname": "Ivanov",
            "surname": "Ivanovich",
            "date_born": "2000-12-12",
            "citizenship": "Россия",
            "russian_passport_no": "1234 567890",
            "international_passport_no": "12 3456789",
            "validity_international_passport": "2024-11-11",
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["firstname"], "Sasha")

    def test_guest_patch(self):
        """Тест для частичного изменения заявки"""

        url = reverse("applications:guest_detail_update_delete", args=(self.guest.pk,))
        data = {
            "firstname": "Sasha",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["firstname"], "Sasha")

    def test_guest_delete(self):
        """Тест на удаление заявки"""

        url = reverse("applications:guest_detail_update_delete", args=(self.guest.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Guest.objects.count(), 0)



