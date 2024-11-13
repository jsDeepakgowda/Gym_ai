# categories.py

# Define food categories and food items with their nutritional information (calories, protein, fat)
FOOD_CATEGORIES = {
    'vegetables': [
        {'name': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4},
        {'name': 'Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6},
        {'name': 'Carrot', 'calories': 41, 'protein': 0.9, 'fat': 0.2},
        {'name': 'Kale', 'calories': 49, 'protein': 4.3, 'fat': 0.9},
    ],
    'nuts': [
        {'name': 'Almonds', 'calories': 575, 'protein': 21, 'fat': 49},
        {'name': 'Cashews', 'calories': 553, 'protein': 18, 'fat': 44},
        {'name': 'Walnuts', 'calories': 654, 'protein': 15, 'fat': 65},
    ],
    'meats': [
        {'name': 'Chicken Breast', 'calories': 165, 'protein': 31, 'fat': 3.6},
        {'name': 'Salmon', 'calories': 206, 'protein': 22, 'fat': 12},
        {'name': 'Beef Steak', 'calories': 242, 'protein': 22, 'fat': 17},
    ],
    'fruits': [
        {'name': 'Banana', 'calories': 89, 'protein': 1.1, 'fat': 0.3},
        {'name': 'Apple', 'calories': 52, 'protein': 0.3, 'fat': 0.2},
        {'name': 'Orange', 'calories': 47, 'protein': 0.9, 'fat': 0.1},
    ],
    'grains': [
        {'name': 'Oats', 'calories': 389, 'protein': 16.9, 'fat': 6.9},
        {'name': 'Quinoa', 'calories': 120, 'protein': 4.1, 'fat': 1.9},
        {'name': 'Brown Rice', 'calories': 111, 'protein': 2.6, 'fat': 0.9},
    ],
}

def get_food_by_category(category):
    """Retrieve foods by category."""
    return FOOD_CATEGORIES.get(category, [])
