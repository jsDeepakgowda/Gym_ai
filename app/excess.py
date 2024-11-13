def calculate_bmi(weight, height):
    """Calculate BMI based on weight (kg) and height (cm)."""
    height_m = height / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    return bmi

def calculate_tdee(weight, height, age, gender):
    """Calculate Total Daily Energy Expenditure (TDEE) based on Mifflin-St Jeor equation."""
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    # Assuming a moderate activity level (can adjust based on user activity level)
    tdee = bmr * 1.55
    return tdee

def categorize_fitness_level(bmi, age):
    """Categorize the user’s fitness level based on BMI and age."""
    if bmi < 18.5:
        return 'underweight'
    elif 18.5 <= bmi < 24.9:
        if age < 25:
            return 'beginner'
        elif 25 <= age < 40:
            return 'intermediate'
        else:
            return 'advanced'
    elif 25 <= bmi < 29.9:
        return 'overweight'
    else:
        return 'obese'

def generate_detailed_workout_plan(goal, fitness_level):
    """Generate a detailed workout plan based on the user’s goal and fitness level."""
    
    # Define sample workout plans based on goal and fitness level
    plans = {
        'weight_loss': {
            'beginner': {
                'exercises': ['Cardio (30 min)', 'Bodyweight Squats', 'Jumping Jacks'],
                'sets': '3 sets of each',
                'frequency': '3-4 times per week',
                'calories_burned': '200-300 calories per session'
            },
            'intermediate': {
                'exercises': ['Running (30 min)', 'Push-ups', 'Mountain Climbers'],
                'sets': '4 sets of each',
                'frequency': '4-5 times per week',
                'calories_burned': '400-500 calories per session'
            },
            'advanced': {
                'exercises': ['HIIT (45 min)', 'Burpees', 'Jump Rope'],
                'sets': '5 sets of each',
                'frequency': '5-6 times per week',
                'calories_burned': '600-700 calories per session'
            }
        },
        'muscle_gain': {
            'beginner': {
                'exercises': ['Bodyweight Squats', 'Push-ups', 'Dumbbell Rows'],
                'sets': '3 sets of 12-15 reps',
                'frequency': '3 times per week',
                'calories_burned': '150-200 calories per session'
            },
            'intermediate': {
                'exercises': ['Squats', 'Deadlifts', 'Bench Press'],
                'sets': '4 sets of 8-10 reps',
                'frequency': '4 times per week',
                'calories_burned': '250-300 calories per session'
            },
            'advanced': {
                'exercises': ['Deadlifts', 'Squats', 'Power Cleans'],
                'sets': '5 sets of 5 reps',
                'frequency': '5 times per week',
                'calories_burned': '350-400 calories per session'
            }
        },
        'endurance': {
            'beginner': {
                'exercises': ['Jogging (30 min)', 'Swimming', 'Cycling'],
                'sets': '3 sets of 5 minutes each',
                'frequency': '3-4 times per week',
                'calories_burned': '250-300 calories per session'
            },
            'intermediate': {
                'exercises': ['Running (45 min)', 'Rowing', 'Mountain Biking'],
                'sets': '4 sets of 10 minutes each',
                'frequency': '4-5 times per week',
                'calories_burned': '400-450 calories per session'
            },
            'advanced': {
                'exercises': ['Marathon Training', 'Ultra Endurance Cycling', 'HIIT'],
                'sets': '5 sets of 15 minutes each',
                'frequency': '5-6 times per week',
                'calories_burned': '500-600 calories per session'
            }
        }
    }

    # Select workout plan based on goal and fitness level
    plan = plans.get(goal, {}).get(fitness_level, {})
    return plan
