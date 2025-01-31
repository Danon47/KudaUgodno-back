import os
from django.core.management.base import BaseCommand
from hotels.models.room.models_room_caterogy import RoomCategory
from users.models import User


class Command(BaseCommand):
    help = "Заполняет базу данных начальными данными"

    def handle(self, *args, **kwargs):
        # Данные удобств отелей, номеров, категорий
        category_rooms = [
            {"name": "Стандарт"},
            {"name": "Комфорт"},
            {"name": "Семейный"},
            {"name": "Люкс"},
        ]

        # Проверяем, заполнены ли уже данные
        if RoomCategory.objects.exists():
            self.stdout.write(self.style.WARNING("=== BD already has these values ==="))
        else:
            for category in category_rooms:
                RoomCategory.objects.get_or_create(**category)

            self.stdout.write(self.style.SUCCESS("=== BD DONE ==="))

        # Создание администратора
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        # Проверяем, существует ли уже администратор с указанным именем пользователя
        if not User.objects.filter(email=os.getenv("ADMIN_EMAIL")).exists():
            # Создаем администратора
            user = User.objects.create(
                email=email,
                is_staff=True,
                is_superuser=True,
                is_active=True,
                first_name="Admin",
                last_name="Admin",
            )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"=== Admin {os.getenv('ADMIN_EMAIL')} successfully created ==="
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"=== Admin with email {os.getenv('ADMIN_EMAIL')} already exists ==="
                )
            )
