from flask import Flask, render_template, Response, request, jsonify,send_file,send_from_directory
from video_analysis import VideoAnalysis
import cv2
import os
import csv
from diete import *
from datetime import datetime
import csv
from io import StringIO
from categories import FOOD_CATEGORIES
from chat import get_response




app = Flask(__name__)
video_analyzer = None
video_mode = 'upload'  # Default mode set to 'upload' for analyzing uploaded videos

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to the CSV file where workout history will be saved
WORKOUT_HISTORY_FILE = 'workout_history.csv'

# File paths for saving diet and workout plans
DIET_PLAN_FOLDER = 'diet_plans'  # Folder where diet plans will be stored
DIET_PLAN_FILE = 'diet_plan.csv'  
WORKOUT_PLAN_FILE = 'workout_plan_history.csv'

if not os.path.exists(DIET_PLAN_FOLDER):
    os.makedirs(DIET_PLAN_FOLDER)
    
def save_diet_plan_to_csv(user_id, diet_plan_type, meal_type, meal_data, timestamp):
    """Save user-selected diet plan to CSV."""
    if not os.path.exists(DIET_PLAN_FILE):
        with open(DIET_PLAN_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'diet_plan_type', 'meal_type', 'meal_data', 'timestamp'])

    with open(DIET_PLAN_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, diet_plan_type, meal_type, meal_data, timestamp])

def save_workout_plan_to_csv(user_id, workout_plan_type, workout_type, timestamp):
    """Save user-selected workout plan to CSV."""
    if not os.path.exists(WORKOUT_PLAN_FILE):
        with open(WORKOUT_PLAN_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'workout_plan_type', 'workout_type', 'timestamp'])

    with open(WORKOUT_PLAN_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, workout_plan_type, workout_type, timestamp])

def save_to_csv(user_id, exercise_type, reps, calories, timestamp):
    """Function to save workout data to CSV. Creates the file if it doesn't exist."""
    if not os.path.exists(WORKOUT_HISTORY_FILE):
        with open(WORKOUT_HISTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'exercise_type', 'reps', 'calories_burned', 'timestamp'])

    with open(WORKOUT_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, exercise_type, reps, calories, timestamp])

def read_workout_history():
    """Function to read workout history from CSV. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(WORKOUT_HISTORY_FILE):
        return []
    with open(WORKOUT_HISTORY_FILE, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)[1:]  # Skip the header row

@app.route('/')
def index():
    """Home page with options to start and stop analysis for uploaded video or live webcam."""
    return render_template('home.html')

@app.route('/progress')
def progress():
    """Display progress (reps and calories) over time in a chart."""
    workouts = read_workout_history()
    progress_data = generate_progress_data(workouts)
    return render_template('progress.html', progress_data=progress_data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/excess')
def excess():
    return render_template('excess.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')
@app.route('/videoanalysis')
def videoanalysis():
    """Page to perform video analysis."""
    return render_template('videoanalysis.html')

@app.route('/recamend')
def recamend():
    """Page to perform video analysis."""
    return render_template('recamend.html')
@app.route('/history')
def history():
    """Display workout history."""
    workouts = read_workout_history()
    return render_template('history.html', workouts=workouts)

def generate_progress_data(workouts):
    """Function to process workout history and generate progress data."""
    dates = []
    reps = []
    calories = []
    for workout in workouts:
        dates.append(workout[4])  # Timestamp of the workout
        reps.append(int(workout[2]))  # Reps
        calories.append(float(workout[3]))  # Calories burned
    return {"dates": dates, "reps": reps, "calories": calories}

def gen_frames(analyzer, exercise_type):
    """Generator function to stream frames from the video analyzer."""
    for frame in analyzer.analyze_video(exercise_type):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/start_analysis', methods=['POST'])
def start_analysis():
    """Start video analysis based on selected mode (upload or webcam)."""
    global video_analyzer, video_mode
    exercise_type = request.form.get('exercise_type', 'push-up')
    video_mode = request.form.get('video_mode', 'upload')  # Check mode

    if video_mode == 'upload':
        # Handle uploaded video file
        video_file = request.files['video_file']
        video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(video_path)
        video_analyzer = VideoAnalysis(video_path=video_path)
    else:
        # Use live webcam feed (camera index 0)
        video_analyzer = VideoAnalysis(video_path=0)

    return jsonify({"status": "Analysis started"}), 200

@app.route('/video_feed')
def video_feed():
    """Route to stream video feed to frontend."""
    global video_analyzer
    exercise_type = request.args.get('exercise_type', 'push-up')  # Get exercise type
    if video_analyzer:
        return Response(gen_frames(video_analyzer, exercise_type),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Video feed not available", 404

@app.route('/stop_analysis', methods=['POST'])
def stop_analysis():
    """Stop video analysis and provide a summary, then save to workout history."""
    global video_analyzer
    if video_analyzer:
        calories, reps = video_analyzer.get_summary()  # Retrieve summary data
        user_id = 1  # Example user ID, replace with actual user ID if using authentication
        exercise_type = 'push-up'  # Example exercise type, change based on input
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp

        # Save the data to CSV
        save_to_csv(user_id, exercise_type, reps, calories, timestamp)

        video_analyzer = None  # Reset the analyzer instance
        return jsonify({"calories_burned": calories, "total_count": reps})
    return jsonify({"error": "No analysis in progress."})

@app.route('/current')
def current():
    """Provides real-time progress data for reps and calories burned."""
    if video_analyzer:
        current_progress = video_analyzer.get_current_progress()
        return jsonify(current_progress)
    return jsonify({
        "current_reps": 0,
        "current_calories": 0,
        "feedback": "No analysis in progress"
    })
    

def save_diet_plan_to_csv(user_id, diet_plan_type, meal_type, meal_data, timestamp):
    """Save user-selected diet plan to CSV."""
    file_path = os.path.join(DIET_PLAN_FOLDER, DIET_PLAN_FILE)
    
    # If the file doesn't exist, create the header row
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'diet_plan_type', 'meal_type', 'meal_data', 'timestamp'])
    
    # Save the diet plan data to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, diet_plan_type, meal_type, meal_data, timestamp])
        
        
@app.post('/predict')
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)

@app.route('/get_diet_plan', methods=['POST'])
def get_diet_plan():
    try:
        # Log the incoming form data for debugging
        print("Received form data:")
        print(request.form)

        # Get input values from the form
        user_id = request.form['user_id']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        goal = request.form['goal']
        activity_level = request.form['activity_level']

        # Generate diet plan
        food_plan, target_calories = generate_diet_plan(weight, height, age, gender, goal, activity_level)

        # Save the diet plan to CSV
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for meal_time, meals in food_plan.items():
            for meal in meals:
                save_diet_plan_to_csv(user_id, goal, meal_time, meal, timestamp)

        # Return the generated diet plan to the user
        return render_template('diet_plan.html', food_plan=food_plan, target_calories=target_calories)

    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/download_diet_plan', methods=['GET'])
def download_diet_plan():
    """Allow the user to download the stored diet plan CSV file."""
    try:
        # Get the full path to the CSV file
        file_path = os.path.join(DIET_PLAN_FOLDER, DIET_PLAN_FILE)
        print(f"File path to download: {file_path}")  # Debugging print

        # Check if the file exists in the directory
        if os.path.exists(file_path):
            print(f"File found. Preparing for download.")  # Debugging print
            # Corrected usage of send_from_directory
            return send_from_directory(directory=DIET_PLAN_FOLDER, filename=DIET_PLAN_FILE, as_attachment=True)
        else:
            print(f"File not found: {file_path}")  # Debugging print
            return jsonify({'error': 'No diet plans found to download.'}), 404
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debugging print
        return jsonify({'error': str(e)}), 500

@app.route('/select_food_categories', methods=['GET'])
def select_food_categories():
    # Passing the food categories to the template
    return render_template('select_food_categories.html', food_categories=FOOD_CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True)
