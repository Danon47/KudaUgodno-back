import os

from django.core.management.base import BaseCommand
from hotels.models import AmenityHotel, AmenityRoom, CategoryRoom
from users.models import User


class Command(BaseCommand):
    help = "Заполняет базу данных начальными данными"

    def handle(self, *args, **kwargs):
        # Данные удобств отелей, номеров, категорий
        amenities_rooms = [
            {
                "name": [
                    "Душ на этаже",
                    "Душ в комнате",
                    "Ванна",
                    "Дополнительная кровать",
                    "Фен",
                    "Сейф",
                    "Чайный набор",
                    "Wi-Fi",
                    "Кондиционер",
                ],
            }
        ]
        amenities_hotel = [
            {
                "name": [
                    "Бассейн",
                    "Собственный пляж",
                    "Семейные номера",
                    "Детский клуб",
                    "Аквапарк",
                    "Теннисный корт",
                    "Бесплатный интернет",
                ],
            }
        ]
        category_rooms = [
            {
                "name": [
                    "Стандарт",
                    "Комфорт",
                    "Семейный",
                    "Люкс",
                ]
            }
        ]

        # Заполняем базу данных
        for amenity_room in amenities_rooms[0]["name"]:
            AmenityRoom.objects.create(name=amenity_room)
        for amenity_hotel in amenities_hotel[0]["name"]:
            AmenityHotel.objects.create(name=amenity_hotel)
        for category_room in category_rooms[0]["name"]:
            CategoryRoom.objects.create(name=category_room)

        self.stdout.write(self.style.SUCCESS("Данные успешно заполнены"))

        # Проверяем, существует ли уже администратор с указанным именем пользователя
        if not User.objects.filter(username=os.getenv("ADMIN_USERNAME")).exists():
            # Создаем администратора
            User.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )

            self.stdout.write(self.style.SUCCESS(f"Администратор {os.getenv('ADMIN_USERNAME')} успешно создан"))
        else:
            self.stdout.write(self.style.WARNING(f"Администратор с именем пользователя {os.getenv('ADMIN_USERNAME')} уже существует"))