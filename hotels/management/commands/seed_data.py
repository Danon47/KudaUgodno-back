import os

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Заполняет базу данных начальными данными"

    def handle(self, *args, **kwargs):
        # Создание администратора
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        # Проверяем, существует ли уже администратор с указанным именем пользователя
        if not User.objects.filter(email=os.getenv("ADMIN_EMAIL")).exists():
            # Создаем администратора
            user = User.objects.create_superuser(
                email=email,
                first_name="Admin",
                last_name="Admin",
            )
            user.set_password(password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f"=== Admin {os.getenv('ADMIN_EMAIL')} successfully created ==="))
        else:
            self.stdout.write(
                self.style.WARNING(f"=== Admin with email {os.getenv('ADMIN_EMAIL')} already exists ===")
            )
