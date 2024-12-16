import os
from django.core.management.base import BaseCommand
from hotels.models import HotelAmenity, RoomAmenity, RoomCategory
from users.models import User


class Command(BaseCommand):
    help = "Заполняет базу данных начальными данными"

    def handle(self, *args, **kwargs):
        # Данные удобств отелей, номеров, категорий
        amenities_rooms = [
            "Душ на этаже",
            "Душ в комнате",
            "Ванна",
            "Дополнительная кровать",
            "Фен",
            "Сейф",
            "Чайный набор",
            "Wi-Fi",
            "Кондиционер",
        ]
        amenities_hotel = [
            "Бассейн",
            "Собственный пляж",
            "Семейные номера",
            "Детский клуб",
            "Аквапарк",
            "Теннисный корт",
            "Бесплатный интернет",
        ]
        category_rooms = [
            "Стандарт",
            "Комфорт",
            "Семейный",
            "Люкс",
        ]

        # Заполняем базу данных
        RoomAmenity.objects.bulk_create(
            [RoomAmenity(name=amenity) for amenity in amenities_rooms]
        )
        HotelAmenity.objects.bulk_create(
            [HotelAmenity(name=amenity) for amenity in amenities_hotel]
        )
        RoomCategory.objects.bulk_create(
            [RoomCategory(name=category) for category in category_rooms]
        )

        self.stdout.write(self.style.SUCCESS("Данные успешно заполнены"))

        # Проверяем, существует ли уже администратор с указанным именем пользователя
        if not User.objects.filter(username=os.getenv("ADMIN_USERNAME")).exists():
            # Создаем администратора
            user = User.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME"),
            )
            user.set_password(os.getenv("ADMIN_PASSWORD"))

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
