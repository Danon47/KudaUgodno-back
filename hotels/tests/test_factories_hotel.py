import pytest
from all_fixture.tests.hotels_factories import HotelFactory, HotelPhotoFactory, HotelRulesFactory


@pytest.mark.django_db
def test_hotel_creation():
    hotel = HotelFactory()
    assert hotel.pk is not None
    assert hotel.name is not None
    assert hotel.star_category is not None
    assert hotel.place is not None
    assert hotel.country is not None
    assert hotel.city is not None
    assert hotel.address is not None
    assert hotel.distance_to_the_station is not None
    assert hotel.distance_to_the_sea is not None
    assert hotel.distance_to_the_center is not None
    assert hotel.distance_to_the_metro is not None
    assert hotel.distance_to_the_airport is not None
    assert hotel.description is not None
    assert hotel.check_in_time is not None
    assert hotel.check_out_time is not None
    assert hotel.amenities_common is not None
    assert hotel.amenities_in_the_room is not None
    assert hotel.amenities_sports_and_recreation is not None
    assert hotel.amenities_for_children is not None
    assert hotel.type_of_meals_ultra_all_inclusive is not None
    assert hotel.type_of_meals_all_inclusive is not None
    assert hotel.type_of_meals_full_board is not None
    assert hotel.type_of_meals_half_board is not None
    assert hotel.type_of_meals_only_breakfast is not None
    assert hotel.user_rating is not None
    assert hotel.type_of_rest is not None
    assert hotel.is_active is not None
    assert hotel.room_categories is not None


@pytest.mark.django_db
def test_hotel_photo_creation():
    hotel_photo = HotelPhotoFactory()
    assert hotel_photo.pk is not None
    assert hotel_photo.hotel is not None
    assert hotel_photo.photo is not None


@pytest.mark.django_db
def test_hotel_rules_creation():
    hotel_rules = HotelRulesFactory()
    assert hotel_rules.pk is not None
    assert hotel_rules.hotel is not None
    assert hotel_rules.name is not None
    assert hotel_rules.description is not None
