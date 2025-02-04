from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserAPITests(APITestCase):
    """
    Тесты для приложения users.
    Проверяем базовый CRUD и корректную работу модельной валидации (clean()).
    Также проверяем forbidden words валидатор.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.ru",
            password="test_password",
            phone_number="+79999999999",
            is_active=True
        )
        # Если нужно, чтобы тесты считали нас авторизованными этим пользователем:
        self.client.force_authenticate(user=self.user)

    def test_user(self):
        """Тест базовых атрибутов самой модели Пользователя"""
        self.assertEqual(self.user.email, "test@test.ru")
        self.assertEqual(self.user.phone_number, "+79999999999")
        self.assertFalse(self.user.first_name)
        self.assertFalse(self.user.last_name)
        self.assertFalse(self.user.description)
        self.assertFalse(self.user.address)
        self.assertFalse(self.user.avatar)
        self.assertEqual(self.user.role, "Пользователь")

    def test_user_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)

        # status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # При пагинации DRF:
        # 'count' = всего записей
        # 'results' = список пользователей
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

        # Убедимся, что в базе 1 пользователь
        self.assertEqual(User.objects.count(), 1)

    def test_user_create(self):
        """Тест создания пользователя (POST /users/)"""
        url = reverse("users:user-list")
        data = {
            "email": "user@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_forbidden_word_validator(self):
        """
        Тест на проверку запрещенных слов.
        Если в first_name будет "плохое_слово", ForbiddenWordValidator должен вернуть 400.
        """
        url = reverse("users:user-list")
        data = {
            "email": "test1@test.ru",
            "first_name": "плохое_слово",  # Должно вызывать 400
        }
        response = self.client.post(url, data)
        # Ожидаем код 400, если валидация срабатывает
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверяем, что в тексте ошибки есть фрагмент про «недопустимое слово»
        self.assertIn("Введено недопустимое слово", str(response.data))

    def test_fill_fields_validator(self):
        """
        Тест на проверку заполнения полей в зависимости от роли (model.clean()).
        Для role=USER нельзя заполнять username, address, description.
        """
        url = reverse("users:user-list")
        data = {
            "email": "test1@test.ru",
            "description": "test",  # Должно быть нельзя при role=USER
        }
        response = self.client.post(url, data)
        # Ожидаем код 400 при некорректном заполнении
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Текст ошибки из model.clean()
        self.assertIn(
            "У пользователя (role=USER) не могут быть заполнены поля",
            str(response.data)
        )

    def test_user_retrieve(self):
        """Тест получения данных одного пользователя (GET /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)

    def test_user_put(self):
        """Тест полного обновления пользователя (PUT /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        data = {
            "email": "user@example.com",
            "phone_number": "+79999999988",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "+79999999988")

    def test_user_patch(self):
        """Тест частичного обновления пользователя (PATCH /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        data = {
            "phone_number": "+79999999988",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "+79999999988")

    def test_user_destroy(self):
        """Тест на удаление пользователя (DELETE /users/{id}/)"""
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.exists())  # Пользователь удалён
