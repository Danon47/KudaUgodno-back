from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+79990000000',
            password='testpassword',
            first_name='Test',
            last_name='User   ',
        )
        self.admin_user = User.objects.create_superuser(
            phone_number='+79991111111',
            password='adminpassword',
            first_name='Admin',
            last_name='Root',
        )
        self.url = reverse('users:user_list_create')  # URL для списка и создания пользователей

    def test_create_user(self):
        self.client.login(phone_number='+79991111111', password='adminpassword')  # Аутентификация администратора
        data = {
            'phone_number': '+79992222222',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User   ',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # Проверка, что пользователь создан

    def test_list_users(self):
        self.client.login(phone_number='+79991111111', password='adminpassword')  # Аутентификация администратора
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Проверка, что два пользователя в списке

    def test_retrieve_user(self):
        self.client.login(phone_number='+79991111111', password='adminpassword')  # Аутентификация администратора
        response = self.client.get(reverse('users:user_retrieve', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], str(self.user.phone_number))

    def test_update_user(self):
        self.client.login(phone_number='+79991111111', password='adminpassword')  # Аутентификация администратора
        data = {
            'phone_number': '+79993333333',
            'password': 'updatedpassword',
            'first_name': 'Updated',
            'last_name': 'User   ',
        }
        response = self.client.put(reverse('users:user_update', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Обновление объекта пользователя из базы данных
        self.assertEqual(str(self.user.phone_number), '+79993333333')

    def test_destroy_user(self):
        self.client.login(phone_number='+79991111111', password='adminpassword')  # Аутентификация администратора
        response = self.client.delete(reverse('users:user_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)  # Проверка, что пользователь удален
