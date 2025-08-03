from django.core.exceptions import ValidationError
from django.test import TestCase

from all_fixture.choices import RoleChoices
from users.models import User


class UserModelTests(TestCase):
    """Тесты для модели пользователя."""

    def setUp(self):
        """Создаем тестовых пользователей перед каждым тестом."""
        self.user = User.objects.create_user(
            email="user@example.com",
            password="userpassword",
            first_name="Обычный",
            last_name="Пользователь",
            phone_number="+79991234567",
            birth_date="1995-07-20",
            role=RoleChoices.USER,
        )

        self.tour_operator = User.objects.create_user(
            email="tour@example.com",
            password="tourpassword",
            first_name="Тур",
            last_name="Оператор",
            phone_number="+79997654321",
            birth_date="1988-05-10",
            role=RoleChoices.TOUR_OPERATOR,
            company_name="Туризм LLC",
            documents="fake_path/document.pdf",
        )

        self.hotel_owner = User.objects.create_user(
            email="hotel@example.com",
            password="hotelpassword",
            first_name="Отель",
            last_name="Владелец",
            phone_number="+79993216548",
            birth_date="1982-03-15",
            role=RoleChoices.HOTELIER,
            company_name="Гостиница ООО",
            documents="fake_path/license.pdf",
        )

        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
        )
        self.admin_user.role = RoleChoices.ADMIN
        self.admin_user.save()

    def test_user_creation(self):
        """Тест на создание обычного пользователя."""
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.role, RoleChoices.USER)
        # Проверяем, что company_name и documents пустые
        self.assertIsNone(self.user.company_name)
        self.assertFalse(self.user.documents)

    def test_tour_operator_creation(self):
        """Тест на создание туроператора."""
        self.assertEqual(self.tour_operator.email, "tour@example.com")
        self.assertEqual(self.tour_operator.role, RoleChoices.TOUR_OPERATOR)
        self.assertEqual(self.tour_operator.company_name, "Туризм LLC")
        self.assertEqual(self.tour_operator.documents, "fake_path/document.pdf")

    def test_hotel_owner_creation(self):
        """Тест на создание владельца отеля."""
        self.assertEqual(self.hotel_owner.email, "hotel@example.com")
        self.assertEqual(self.hotel_owner.role, RoleChoices.HOTELIER)
        self.assertEqual(self.hotel_owner.company_name, "Гостиница ООО")
        self.assertEqual(self.hotel_owner.documents, "fake_path/license.pdf")

    def test_admin_creation(self):
        """Тест на создание администратора."""
        self.assertEqual(self.admin_user.email, "admin@example.com")
        self.assertEqual(self.admin_user.role, RoleChoices.ADMIN)
        self.assertTrue(self.admin_user.is_superuser)

    def test_user_string_representation(self):
        """Тест на строковое представление объекта пользователя."""
        self.assertEqual(str(self.user), "user@example.com")

    def test_clean_user_role(self):
        """Проверка валидации: обычный пользователь не может иметь company_name и documents."""
        self.user.company_name = "Тестовая компания"
        self.user.documents = "fake_path/test.pdf"
        with self.assertRaises(ValidationError) as error:
            self.user.full_clean()
        self.assertIn(
            "У обычного пользователя не могут быть заполнены поля: company_name, documents.", str(error.exception)
        )

    def test_clean_tour_operator_role(self):
        """Проверка валидации: туроператор должен указывать company_name и documents."""
        self.tour_operator.company_name = None
        with self.assertRaises(ValidationError) as error:
            self.tour_operator.full_clean()
        self.assertIn(
            "Для Туроператора и Отельера поле 'Название компании' является обязательным.", str(error.exception)
        )

        self.tour_operator.company_name = "Туризм LLC"
        self.tour_operator.documents = None
        with self.assertRaises(ValidationError) as error:
            self.tour_operator.full_clean()
        self.assertIn("Для Туроператора и Отельера необходимо загрузить документы.", str(error.exception))

    def test_clean_hotel_owner_role(self):
        """Проверка валидации: отельер должен указывать company_name и documents."""
        self.hotel_owner.company_name = None
        with self.assertRaises(ValidationError) as error:
            self.hotel_owner.full_clean()
        self.assertIn(
            "Для Туроператора и Отельера поле 'Название компании' является обязательным.", str(error.exception)
        )

        self.hotel_owner.company_name = "Гостиница ООО"
        self.hotel_owner.documents = None
        with self.assertRaises(ValidationError) as error:
            self.hotel_owner.full_clean()
        self.assertIn("Для Туроператора и Отельера необходимо загрузить документы.", str(error.exception))
