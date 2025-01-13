from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class UserAPITests(APITestCase):
    """Тесты модели User"""

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.ru",
            password="test_password",
            phone_number="+79999999999",
            is_active=True
        )
        self.client.force_authenticate(user=self.user)

    def test_user(self):
        """Тест модели Пользователя"""

        self.assertEqual(self.user.email, "test@test.ru")
        self.assertEqual(self.user.phone_number, "+79999999999")
        self.assertFalse(self.user.first_name)
        self.assertFalse(self.user.last_name)
        self.assertFalse(self.user.description)
        self.assertFalse(self.user.address)
        self.assertFalse(self.user.avatar)
        self.assertEqual(self.user.role, "Пользователь")

    def test_user_list(self):
        """Тест на вывод списка пользователей"""

        url = reverse("users:user_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_user_create(self):
        """Тест создания пользователя"""

        url = reverse("users:user_list_create")
        data = {
            "email": "user@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_forbidden_word_validator(self):
        """Тест на проверку запрещенных слов"""

        url = reverse("users:user_list_create")
        data = {
            "email": "test1@test.ru",
            "first_name": "плохое_слово",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["non_field_errors"][0], "Введено недопустимое слово")

    def test_fill_fields_validator(self):
        """Тест на проверку заполнения полей"""

        url = reverse("users:user_list_create")
        data = {
            "email": "test1@test.ru",
            "description": "test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["non_field_errors"][0], "У пользователя не могут быть заполнены поля: username, address, description")

    def test_user_retrieve(self):
        """Тест на вывод конкретного пользователя"""

        url = reverse("users:user_name_detail", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)

    def test_user_put(self):
        """Тест на полное обновление пользователя"""

        url = reverse("users:user_name_detail", args=(self.user.id,))
        data = {
            "email": "user@example.com",
            "phone_number": "+79999999988",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "+79999999988")

    def test_user_patch(self):
        """Тест на частичное обновление пользователя"""

        url = reverse("users:user_name_detail", args=(self.user.id,))
        data = {
            "phone_number": "+79999999988",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "+79999999988")

    def test_user_destroy(self):
        """Тест на удаление пользователя"""

        url = reverse("users:user_name_detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.count())  # Проверка, что пользователь удален
