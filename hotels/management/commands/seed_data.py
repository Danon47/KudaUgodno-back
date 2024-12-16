import os
from django.core.management.base import BaseCommand
from hotels.models import HotelAmenity, RoomAmenity, RoomCategory
from users.models import User


class Command(BaseCommand):
    help = "Заполняет базу данных начальными данными"

    def handle(self, *args, **kwargs):
        # Данные удобств отелей, номеров, категорий
        amenities_room = [
            {"name": "Душ на этаже"},
            {"name": "Душ в комнате"},
            {"name": "Ванна"},
            {"name": "Дополнительная кровать"},
            {"name": "Фен"},
            {"name": "Сейф"},
            {"name": "Чайный набор"},
            {"name": "Wi-Fi"},
            {"name": "Кондиционер"},
        ]

        amenities_hotel = [
            {"name": "Бассейн"},
            {"name": "Собственный пляж"},
            {"name": "Семейные номера"},
            {"name": "Детский клуб"},
            {"name": "Аквапарк"},
            {"name": "Теннисный корт"},
            {"name": "Бесплатный интернет"},
        ]

        category_rooms = [
            {"name": "Стандарт"},
            {"name": "Комфорт"},
            {"name": "Семейный"},
            {"name": "Люкс"},
        ]

        # Проверяем, заполнены ли уже данные
        if RoomAmenity.objects.exists() or HotelAmenity.objects.exists() or RoomCategory.objects.exists():
            self.stdout.write(self.style.WARNING("=== BD already has these values ==="))
        else:

            # Заполняем базу данных
            for amenity in amenities_room:
                RoomAmenity.objects.get_or_create(**amenity)

            for amenity in amenities_hotel:
                HotelAmenity.objects.get_or_create(**amenity)

            for category in category_rooms:
                RoomCategory.objects.get_or_create(**category)

            self.stdout.write(self.style.SUCCESS("=== BD DONE ==="))

        # Создание администратора
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        # Проверяем, существует ли уже администратор с указанным именем пользователя
        if not User.objects.filter(username=os.getenv("ADMIN_USERNAME")).exists():
            # Создаем администратора
            user = User.objects.create_superuser(
                username=username,
            )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Администратор {os.getenv('ADMIN_USERNAME')} успешно создан"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Администратор с именем пользователя {os.getenv('ADMIN_USERNAME')} уже существует"
                )
            )
