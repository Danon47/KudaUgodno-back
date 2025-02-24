import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from hotels.choices import PlaceChoices, TypeOfHolidayChoices
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.room.models_room import Room

class Command(BaseCommand):
    help = "Populate the database with test hotels and rooms"

    def handle(self, *args, **kwargs):
        hotels = self.create_test_hotels(1)
        self.create_test_rooms(hotels)
        self.stdout.write(self.style.SUCCESS("Тестовые отели и номера заполнены"))

    def create_test_hotels(self, count):
        places = [choice[0] for choice in PlaceChoices.choices]
        types_of_holiday = [choice[0] for choice in TypeOfHolidayChoices.choices]
        countries = ["США", "Россия", "Франция", "Италия", "Испания"]
        cities = ["Майами", "Москва", "Париж", "Рим", "Мадрид"]
        room_categories = ["Стандарт", "Делюкс", "Полулюкс", "Семейный"]
        rules = {
            "С животными": "Можно если за ними следить",
            "Бухать": "Можно если за Вами следит жена"
        }


        hotels = []
        for i in range(count):
            hotel = Hotel.objects.create(
                name=f"Отель под номером {i+1}",
                star_category=random.randint(1, 5),
                place=random.choice(places),
                country=random.choice(countries),
                city=random.choice(cities),
                address=f"Ул. Пушкина, д. {i+1}",
                distance_to_the_station=random.randint(0, 50000),
                distance_to_the_sea=random.randint(0, 50000),
                distance_to_the_center=random.randint(0, 50000),
                distance_to_the_metro=random.randint(0, 50000),
                distance_to_the_airport=random.randint(0, 50000),
                description=f"Так себе описание отеля под номером {i+1}",
                check_in_time=timezone.now().time(),
                check_out_time=timezone.now().time(),
                type_of_meals_ultra_all_inclusive=random.randint(3000, 10000),
                type_of_meals_all_inclusive=random.randint(3000, 8000),
                type_of_meals_full_board=random.randint(2000, 5000),
                type_of_meals_half_board=random.randint(2000, 2500),
                type_of_meals_only_breakfast=random.randint(100, 1000),
                user_rating=round(random.uniform(2, 9), 1),
                type_of_rest=random.choice(types_of_holiday),
                is_active=random.choice([True, False]),
                room_categories=random.sample(room_categories, k=random.randint(1, len(room_categories))),
            )
            hotels.append(hotel)

            for rule_name, rule_description in rules.items():
                HotelRules.objects.create(
                    hotel=hotel,
                    name=rule_name,
                    description=rule_description,
                )
        return hotels

    def create_test_rooms(self, hotels):
        room_categories = ["Стандарт", "Делюкс", "Полулюкс", "Семейный"]
        amenities_common = ["WiFi", "ТВ", "Минибар", "Кондиционер"]
        amenities_coffee = ["Кофе машина в номере", "Чайный сет"]
        amenities_bathroom = ["Душевые принадлежности", "Фен"]
        amenities_view = ["Море", "Горы", "Сад"]

        for hotel in hotels:
            for _ in range(random.randint(1, 3)):  # Для каждого отеля создаем от 1 до 3 номеров
                Room.objects.create(
                    hotel=hotel,
                    category=random.choice(room_categories),
                    price=random.randint(1000, 50000),
                    type_of_meals=["Только завтраки", "Полупансион", "Ультра всё включено"],
                    number_of_adults=random.randint(1, 4),
                    number_of_children=random.randint(1, 4),
                    single_bed=random.randint(1, 3),
                    double_bed=random.randint(1, 3),
                    area=random.randint(20, 100),
                    quantity_rooms=random.randint(1, 10),
                    amenities_common=random.sample(amenities_common, k=random.randint(1, len(amenities_common))),
                    amenities_coffee=random.sample(amenities_coffee, k=random.randint(0, len(amenities_coffee))),
                    amenities_bathroom=random.sample(amenities_bathroom, k=random.randint(1, len(amenities_bathroom))),
                    amenities_view=random.sample(amenities_view, k=random.randint(1, len(amenities_view))),
                )
