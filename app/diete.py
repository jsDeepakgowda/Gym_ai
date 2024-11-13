def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender")

# Function to calculate TDEE (Total Daily Energy Expenditure)
def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

# Function to get food recommendations based on the goal
def get_food_recommendations(goal, target_calories):
    food_plan = {
        'lose-weight': {
            'breakfast': ['Oatmeal with almond butter and a banana', 'Egg whites with spinach and whole-wheat toast'],
            'lunch': ['Grilled chicken breast with quinoa and broccoli', 'Salmon with sweet potato'],
            'dinner': ['Baked cod with steamed asparagus', 'Chicken stir-fry with bell peppers and brown rice']
        },
        'gain-muscle': {
            'breakfast': ['Scrambled eggs with avocado and whole-grain toast', 'Greek yogurt with granola'],
            'lunch': ['Grilled steak with sweet potato and steamed broccoli', 'Chicken with quinoa'],
            'dinner': ['Salmon with asparagus', 'Beef stir-fry with bell peppers and brown rice']
        },
        'maintain-weight': {
            'breakfast': ['Whole-grain pancakes with strawberries', 'Greek yogurt with oats'],
            'lunch': ['Turkey sandwich with lettuce and whole-wheat bread', 'Grilled chicken salad'],
            'dinner': ['Pasta with marinara sauce and lean turkey', 'Grilled chicken with roasted potatoes']
        }
    }
    return food_plan.get(goal, {})

# Function to generate the diet plan
def generate_diet_plan(weight, height, age, gender, goal, activity_level):
    # Calculate BMR and TDEE
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    # Adjust for goal
    if goal == 'lose-weight':
        target_calories = tdee - 500  # 500 calorie deficit for weight loss
    elif goal == 'gain-muscle':
        target_calories = tdee + 500  # 500 calorie surplus for muscle gain
    elif goal == 'maintain-weight':
        target_calories = tdee  # No change for maintenance
    else:
        raise ValueError("Invalid goal")

    # Get food recommendations
    food_plan = get_food_recommendations(goal, target_calories)

    # Return the food plan and target calories
    return food_plan, target_calories
