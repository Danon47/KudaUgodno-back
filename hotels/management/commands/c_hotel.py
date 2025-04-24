import os
import random
from datetime import date, time, timedelta

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from all_fixture.choices import PlaceChoices, TypeOfHolidayChoices
from flights.models import Flight
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_photo import RoomPhoto
from tours.models import Tour, TourStock
from users.models import User


class Command(BaseCommand):
    help = "Команда по добавлению рандомной инфы по всем сущностям"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            hotels = self.create_test_hotels(10)
            rooms = self.create_test_rooms(hotels)
            flights = self.create_flights()
            tours = self.create_test_tours(flights, hotels, rooms)
            self.print_success_message(len(hotels), len(flights), len(tours))

    def print_success_message(self, hotels_count, flights_count, tours_count):
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано:\n"
                f"- {hotels_count} отелей c 4 фото в каждом\n"
                f"- {hotels_count*5} номеров с 6 фото каждом\n"
                f"- {flights_count} рейсов\n"
                f"- {tours_count} туров\n"
            )
        )

    def add_photos(self, instances, dir_path, photo_model, fk_name, count):
        files = os.listdir(dir_path)
        for obj in instances:
            for _ in range(count):
                filename = random.choice(files)
                full_path = os.path.join(dir_path, filename)
                with open(full_path, "rb") as f:
                    django_file = File(f, name=filename)
                    photo_model.objects.create(**{fk_name: obj}, photo=django_file)

    def create_test_hotels(self, count):
        places = [choice[0] for choice in PlaceChoices.choices]
        types_of_holiday = [choice[0] for choice in TypeOfHolidayChoices.choices]

        countries_cities = {
            "Турция": ["Анталия", "Стамбул", "Измир"],
            "Греция": ["Афины", "Салоники", "Ираклион"],
            "Франция": ["Париж", "Ницца", "Марсель"],
            "Италия": ["Рим", "Милан", "Венеция"],
            "Испания": ["Мадрид", "Барселона", "Валенсия"],
            "Кипр": ["Лимассол", "Никосия", "Пафос"],
            "Россия": ["Москва", "Санкт-Петербург"],
        }

        room_categories = ["Стандарт", "Делюкс", "Полулюкс", "Семейный"]
        rules = {"С животными": "Можно если за ними следить", "Бухать": "Можно если за Вами следит жена"}
        # Пути к тестовым фотографиям отелей
        hotel_photos_dir = os.path.join(settings.BASE_DIR, "static", "test_hotel")

        hotels = []
        for i in range(count):
            country = random.choice(list(countries_cities.keys()))
            city = random.choice(countries_cities[country])
            hotel = Hotel.objects.create(
                name=f"Отель под номером в {city}",
                star_category=random.randint(1, 5),
                place=random.choice(places),
                country=country,
                city=city,
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
                warm=random.choice([True, False]),
            )
            hotels.append(hotel)

            for rule_name, rule_description in rules.items():
                HotelRules.objects.create(
                    hotel=hotel,
                    name=rule_name,
                    description=rule_description,
                )
        self.add_photos(hotels, hotel_photos_dir, HotelPhoto, "hotel", 4)
        return hotels

    def create_test_rooms(self, hotels, count=5):
        room_categories = ["Стандарт", "Делюкс", "Полулюкс", "Семейный"]
        amenities_common = ["WiFi", "ТВ", "Минибар", "Кондиционер"]
        amenities_coffee = ["Кофе машина в номере", "Чайный сет"]
        amenities_bathroom = ["Душевые принадлежности", "Фен"]
        amenities_view = ["Море", "Горы", "Сад"]

        room_photos_dir = os.path.join(settings.BASE_DIR, "static", "test_room")

        rooms = []
        for hotel in hotels:
            for _ in range(count):
                room = Room.objects.create(
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
                rooms.append(room)

        self.add_photos(rooms, room_photos_dir, RoomPhoto, "room", 6)

        return rooms

    def create_flights(self):
        """
        Создаёт по два рейса для каждого отеля за пределами России:
        — рейс туда (Москва → город отеля)
        — рейс обратно (город отеля → Москва) через 7 дней
        Возвращает список всех созданных Flight.
        """
        arrival_city_airport = {
            # Турция
            "Анталия": "AYT",
            "Стамбул": "IST",
            "Измир": "ADB",
            # Греция
            "Афины": "ATH",
            "Салоники": "SKG",
            "Ираклион": "HER",
            # Франция
            "Париж": "CDG",
            "Ницца": "NCE",
            "Марсель": "MRS",
            # Италия
            "Рим": "FCO",
            "Милан": "MXP",
            "Венеция": "VCE",
            # Испания
            "Мадрид": "MAD",
            "Барселона": "BCN",
            "Валенсия": "VLC",
            # Кипр
            "Лимассол": "LCL",
            "Никосия": "NIC",
            "Пафос": "PFO",
            # Египет
            "Шарм-Эль-Шейх": "SSH",
        }

        flight_numbers = ["AT-5555", "TT-6666", "TQ-7777", "TS-8888"]
        airlines = ["Azure", "Аэрофлот"]
        service_classes = ["Эконом", "Бизнес", "Первый"]
        flight_types = ["Регулярный", "Чартерный"]
        descriptions = ["Багаж включен", "Багаж не включен"]

        created_flights = []

        # Перебираем все отели за пределами России
        for hotel in Hotel.objects.exclude(country="Россия").iterator():
            city = hotel.city
            # Пропускаем, если нет аэропорта для этого города
            if city not in arrival_city_airport:
                continue

            # --- Рейс туда ---
            # Дата в мае 2025, случайный день с 1 по 24
            dep_date = date(2025, 5, random.randint(1, 24))
            dep_time = time(hour=random.randint(0, 23), minute=random.choice([0, 15, 30, 45]))
            arrival_time = self.generate_arrival_time(dep_time, same_day=True)

            flight_to = Flight.objects.create(
                flight_number=random.choice(flight_numbers),
                airline=random.choice(airlines),
                departure_city="Москва",
                departure_airport="SVO",
                arrival_city=city,
                arrival_airport=arrival_city_airport[city],
                departure_date=dep_date,
                departure_time=dep_time,
                arrival_date=dep_date,
                arrival_time=arrival_time,
                price=round(random.uniform(1000, 10000), 2),
                price_for_child=round(random.uniform(500, 5000), 2) if random.random() > 0.3 else None,
                service_class=random.choice(service_classes),
                flight_type=random.choice(flight_types),
                description=random.choice(descriptions),
            )
            created_flights.append(flight_to)

            # --- Рейс обратно через 7 дней ---
            return_date = dep_date + timedelta(days=7)
            return_dep_time = time(hour=random.randint(0, 23), minute=random.choice([0, 15, 30, 45]))
            return_arrival_time = self.generate_arrival_time(return_dep_time, same_day=True)

            flight_back = Flight.objects.create(
                flight_number=random.choice(flight_numbers),
                airline=random.choice(airlines),
                departure_city=city,
                departure_airport=arrival_city_airport[city],
                arrival_city="Москва",
                arrival_airport="SVO",
                departure_date=return_date,
                departure_time=return_dep_time,
                arrival_date=return_date,
                arrival_time=return_arrival_time,
                price=round(random.uniform(1000, 10000), 2),
                price_for_child=round(random.uniform(500, 5000), 2) if random.random() > 0.3 else None,
                service_class=random.choice(service_classes),
                flight_type=random.choice(flight_types),
                description=random.choice(descriptions),
            )
            created_flights.append(flight_back)

        return created_flights

    def generate_arrival_time(self, dep_time, same_day=True):
        """Генерирует реалистичное время прибытия"""
        if same_day:
            arr_hour = random.randint(dep_time.hour, 23)
            if arr_hour == dep_time.hour:
                arr_min = random.randint(dep_time.minute + 1, 59)
            else:
                arr_min = random.choice([0, 15, 30, 45])
        else:
            arr_hour = random.randint(0, 23)
            arr_min = random.choice([0, 15, 30, 45])

        return time(arr_hour, arr_min)

    # def create_tours(self, hotel, rooms, flights):
    #     date_start_end = date(2025, 5, random.randint(1, 15))
    #     Tour.objects.create(
    #         start_date=date_start_end,
    #         end_date=date_start_end + timedelta(days=7),
    #         flight_to=flights,
    #         flight_from=flights,
    #         departure_country=flights.departure_country,
    #         departure_city=flights.departure_city,
    #         arrival_country=flights.arrival_country,
    #         arrival_city=flights.arrival_city,
    #         tour_operator=1,
    #         transfer=random.choice([True, False]),
    #         hotel=hotel,
    #         rooms=rooms,
    #         price=round(random.uniform(10000, 50000), 2),
    #         is_active=random.choice([True, False]),
    #     )

    def create_test_tours(self, flights, hotels, rooms, count=20):
        """
        Генерация тестовых туров.
        :param flights: список всех созданных Flight
        :param hotels: список Hotel
        :param rooms: список Room
        :param count: желаемое число туров
        :return: список созданных Tour
        """
        tours = []
        operators = list(User.objects.filter(role="TOUR_OPERATOR")[:5])

        for _ in range(count):
            # Выбираем пару «туда» и «обратно»
            flight_to = random.choice([f for f in flights if f.departure_city == "Москва"])
            flight_back = random.choice(
                [f for f in flights if f.arrival_city == "Москва" and f.arrival_date > flight_to.departure_date],
            )
            # Даты тура — от вылета до возвращения
            start = flight_to.departure_date
            end = flight_back.departure_date

            hotel = random.choice(hotels)
            room = random.choice(rooms) if random.choice([True, False]) else None

            operator = random.choice(operators) if operators else None

            # Создаём скидку в половине случаев
            stock = None
            if random.random() < 0.5:
                discount = random.randint(5, 30)
                end_stock = end - timedelta(days=random.randint(1, 5))
                stock = TourStock.objects.create(active_stock=True, discount_amount=discount, end_date=end_stock)

            tour = Tour.objects.create(
                start_date=start,
                end_date=end,
                flight_to=flight_to,
                flight_from=flight_back,
                departure_country="Россия",
                departure_city="Москва",
                arrival_country=hotel.country,
                arrival_city=hotel.city,
                tour_operator=operator,
                hotel=hotel,
                room=room.category if room else hotel.room_categories[0],
                transfer=random.choice([True, False]),
                price=round(random.uniform(50000, 200000), 2),
                stock=stock,
                is_active=random.choice([True, False]),
            )
            tours.append(tour)

        return tours
