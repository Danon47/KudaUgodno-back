import factory
from all_fixture.tests.test_temp_image import create_test_image
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules


class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    name = factory.Faker('company')
    star_category = factory.Faker('random_int', min=0, max=5)
    place = factory.Faker('word')
    country = factory.Faker('country')
    city = factory.Faker('city')
    address = factory.Faker('address')
    distance_to_the_station = factory.Faker('random_int', min=0, max=200000)
    distance_to_the_sea = factory.Faker('random_int', min=0, max=200000)
    distance_to_the_center = factory.Faker('random_int', min=0, max=200000)
    distance_to_the_metro = factory.Faker('random_int', min=0, max=200000)
    distance_to_the_airport = factory.Faker('random_int', min=0, max=200000)
    description = factory.Faker('text')
    check_in_time = factory.Faker('time_object')
    check_out_time = factory.Faker('time_object')
    amenities_common = factory.List([factory.Faker('word') for _ in range(3)])
    amenities_in_the_room = factory.List([factory.Faker('word') for _ in range(3)])
    amenities_sports_and_recreation = factory.List([factory.Faker('word') for _ in range(3)])
    amenities_for_children = factory.List([factory.Faker('word') for _ in range(3)])
    type_of_meals_ultra_all_inclusive = factory.Faker('random_int', min=0, max=10000)
    type_of_meals_all_inclusive = factory.Faker('random_int', min=0, max=10000)
    type_of_meals_full_board = factory.Faker('random_int', min=0, max=10000)
    type_of_meals_half_board = factory.Faker('random_int', min=0, max=10000)
    type_of_meals_only_breakfast = factory.Faker('random_int', min=0, max=10000)
    user_rating = factory.Faker('pydecimal', left_digits=2, right_digits=1, positive=True)
    type_of_rest = factory.Faker('word')
    is_active = factory.Faker('boolean')
    room_categories = factory.List([factory.Faker('word') for _ in range(3)])

class HotelPhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelPhoto

    hotel = factory.SubFactory(HotelFactory)
    photo = factory.LazyFunction(create_test_image)

class HotelRulesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelRules

    hotel = factory.SubFactory(HotelFactory)
    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
