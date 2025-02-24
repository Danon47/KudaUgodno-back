from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITests(APITestCase):
    """
    Тесты для приложения users.
    Проверяем базовый CRUD и корректную работу модельной валидации (clean()).
    Также проверяем forbidden words валидатор.
    """

    def setUp(self):
        self.user_data = {
            "username": "ivanov_username",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivanov@example.com",
            "phone_number": "+79999999999",
            "birth_date": "1990-01-01",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_attributes(self):
        """Тест базовых атрибутов самой модели Пользователя"""
        self.assertEqual(self.user.first_name, "Иван")
        self.assertEqual(self.user.last_name, "Иванов")
        self.assertEqual(self.user.email, "ivanov@example.com")
        self.assertEqual(self.user.phone_number.as_e164, "+79999999999")

    def test_create_user(self):
        """Тест создания пользователя (POST /users/)"""
        url = reverse("users:user-list")
        new_user_data = {
            "username": "smirnov_username",
            "first_name": "Мария",
            "last_name": "Смирнова",
            "email": "smirnova@example.com",
            "phone_number": "+79999999988",
            "birth_date": "1985-05-15",
            "password": "newpassword123",
        }
        response = self.client.post(url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_forbidden_word_validator(self):
        """Тест на проверку запрещённых слов."""
        url = reverse("users:user-list")
        data = {
            "username": "badword_username",
            "first_name": "запрещенное_слово",
            "last_name": "Петров",
            "email": "forbidden@example.com",
            "phone_number": "+79999999944",
            "birth_date": "1980-01-01",
            "password": "password123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Введено недопустимое слово", str(response.data))

    def test_clean_method_role_user(self):
        """Тест на проверку заполнения полей в зависимости от роли (model.clean())."""
        self.user.role = "USER"
        self.user.company_name = "Тестовая компания"
        with self.assertRaisesMessage(
            ValidationError, "У обычного пользователя не могут быть заполнены поля: company_name, documents."
        ):
            self.user.full_clean()

    def test_get_user_detail(self):
        """Тест получения данных одного пользователя (GET /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "ivanov@example.com")

    def test_update_user_put(self):
        """Тест полного обновления пользователя (PUT /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        update_data = {
            "username": "updated_username",
            "first_name": "Алексей",
            "last_name": "Смирнов",
            "email": "smirnov@example.com",
            "phone_number": "+79999999977",
            "birth_date": "1985-05-15",
        }
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "smirnov@example.com")

    def test_partial_update_user_patch(self):
        """Тест частичного обновления пользователя (PATCH /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.patch(url, {"first_name": "Алексей"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Алексей")

    def test_delete_user(self):
        """Тест на удаление пользователя (DELETE /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
