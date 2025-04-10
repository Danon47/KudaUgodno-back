import random
from datetime import time

from django.core.management.base import BaseCommand

from all_fixture.choices import PlaceChoices, TypeOfHolidayChoices
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.room.models_room import Room


class Command(BaseCommand):
    help = "Команда по добавлению рандомной инфы по всем сущностям"

    def handle(self, *args, **kwargs):
        hotels = self.create_test_hotels(1)
        self.create_test_rooms(hotels)
        self.stdout.write(
            self.style.SUCCESS(
                """Тестовый отель, с двумя номерам - создан."""
                """Тестовый рейс туда, тестовый рейст обратно - созданы."""
                """Тестовый гость - создан."""
                """Тестовый тур - создан."""
                """Тестовый страховка в ЛК Турагента - создана."""
            )
        )

    def create_test_hotels(self, count):
        places = [choice[0] for choice in PlaceChoices.choices]
        types_of_holiday = [choice[0] for choice in TypeOfHolidayChoices.choices]
        countries = ["США", "Россия", "Франция", "Италия", "Испания"]
        cities = ["Майами", "Москва", "Париж", "Рим", "Мадрид"]
        room_categories = ["Стандарт", "Делюкс", "Полулюкс", "Семейный"]
        rules = {"С животными": "Можно если за ними следить", "Бухать": "Можно если за Вами следит жена"}

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
                check_in_time=time(random.randint(14, 16), 0),
                check_out_time=time(random.randint(10, 12), 0),
                type_of_meals_ultra_all_inclusive=random.randint(3000, 10000),
                type_of_meals_all_inclusive=random.randint(3000, 8000),
                type_of_meals_full_board=random.randint(2000, 5000),
                type_of_meals_half_board=random.randint(2000, 2500),
                type_of_meals_only_breakfast=random.randint(100, 1000),
                user_rating=round(random.uniform(2, 9), 1),
                type_of_rest=random.choice(types_of_holiday),
                is_active=random.choice([True, False]),
                room_categories=random.sample(room_categories, k=random.randint(1, len(room_categories))),
                width=round(random.uniform(-90, 90), 6),
                longitude=round(random.uniform(-180, 180), 6),
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

    # def create_flights(self):
    #     flight_number = [
    #         "AT-5555",
    #         "TT-6666",
    #         "TQ-7777",
    #         "TS-8888",
    #     ]
    #     airline = ["Azure", "Аэрофлот", "S7"]
    #     departure_airport = [
    #         "SVO",
    #         "DME",
    #     ]
    #     arrival_airport = ["AYT", "YRSS"]
    #     departure_date = "2025-06-01"
    #     departure_time = "10:00:00"
    #     arrival_date = "2025-06-01"
    #     arrival_time = "11:00:00"
    #     price = round(random.uniform(1000, 10000), 2)
    #     service_class = ["Эконом", "Бизнес", "Первый"]
    #     flight_type = ["Регулярный", "Чартерный"]
    #     description = ["Багаж включен", "Багаж не включен"]
    #
    #     for flight in flights:
    #         for _ in range(random)
    #
    #
    #
    # def create_tours(self, hotels, flights):
    #     start_date = "2025-06-01"
    #     end_date = "2025-06-02"
    #     #flight_to - self.fligts
    #     #flight_from - self.flights
    #     departure_city =
