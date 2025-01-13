from hotels.choices import MealChoices


def calculate_nightly_prices(room):
    base_price = room.nightly_price
    room.nightly_price_no_meals = base_price
    room.nightly_price_ultra_all_inclusive = 0
    room.nightly_price_all_inclusive = 0
    room.nightly_price_full_board = 0
    room.nightly_price_half_board = 0
    room.nightly_price_only_breakfast = 0

    has_meal_selected = False

    for meal in room.meal.all():
        price_capacities_meal = meal.price_per_person * room.capacity

        has_meal_selected = True
        if meal.name == MealChoices.ULTRA_ALL_INCLUSIVE:
            room.nightly_price_ultra_all_inclusive = base_price + price_capacities_meal
        elif meal.name == MealChoices.ALL_INCLUSIVE:
            room.nightly_price_all_inclusive = base_price + price_capacities_meal
        elif meal.name == MealChoices.FULL_BOARD:
            room.nightly_price_full_board = base_price + price_capacities_meal
        elif meal.name == MealChoices.HALF_BOARD:
            room.nightly_price_half_board = base_price + price_capacities_meal
        elif meal.name == MealChoices.ONLY_BREAKFAST:
            room.nightly_price_only_breakfast = base_price + price_capacities_meal

    if not has_meal_selected:
        room.nightly_price_ultra_all_inclusive = 0
        room.nightly_price_all_inclusive = 0
        room.nightly_price_full_board = 0
        room.nightly_price_half_board = 0
        room.nightly_price_only_breakfast = 0
