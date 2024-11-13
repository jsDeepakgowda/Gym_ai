# suggestions.py

def get_suggestions(exercise_type):
    suggestions = {
        "push-up": [
            {"area": "Posture", "details": "Keep your back straight and avoid slouching to improve your push-up form."},
            {"area": "Hand Placement", "details": "Ensure your hands are placed slightly wider than shoulder-width apart."},
            {"area": "Range of Motion", "details": "Lower your body until your chest nearly touches the ground."},
        ],
        "pull-up": [
            {"area": "Grip", "details": "Use a shoulder-width grip to optimize your pull-up strength."},
            {"area": "Body Position", "details": "Keep your body straight and avoid swinging."},
            {"area": "Pull Technique", "details": "Engage your core and pull from your elbows, not just your arms."},
        ],
        "squat": [
            {"area": "Foot Position", "details": "Keep your feet shoulder-width apart and toes slightly pointed out."},
            {"area": "Depth", "details": "Ensure to squat down until your thighs are parallel to the ground."},
            {"area": "Knee Alignment", "details": "Keep your knees in line with your toes to prevent injury."},
        ],
        "sit-up": [
            {"area": "Neck Position", "details": "Keep your neck neutral to avoid straining."},
            {"area": "Core Engagement", "details": "Engage your core throughout the movement."},
            {"area": "Controlled Movement", "details": "Focus on a controlled motion when lifting your upper body."},
        ],
        "walk": [
            {"area": "Posture", "details": "Stand tall with your shoulders back to improve your walking form."},
            {"area": "Stride", "details": "Maintain a comfortable stride length to enhance efficiency."},
            {"area": "Breathing", "details": "Practice rhythmic breathing to optimize your oxygen intake."},
        ],
    }
    
    return suggestions.get(exercise_type, [])
