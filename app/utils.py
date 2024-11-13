import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
from moviepy.editor import ImageSequenceClip
import os

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) -\
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def detection_body_part(landmarks, body_part_name):
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility
    ]

def detection_body_parts(landmarks):
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])

    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection_body_part(landmarks, lndmrk)
        body_parts.loc[i] = lndmrk, cord[0], cord[1]

    return body_parts

def score_table(exercise_type, frame, counter, status, calories_burned, feedback):
    # Define text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (11, 252, 3)  # Green for exercise details
    feedback_color = (0, 0, 255)  # Red for feedback
    thickness = 3
        
    cv2.putText(frame, f'Exercise: {exercise_type}', (10, 70), font, font_scale, font_color, thickness)
    
    # Overlay counter
    cv2.putText(frame, f'Rep: {counter}', (10,110), font, font_scale, font_color, thickness)
    
    cv2.putText(frame, f'Calories Burned: {calories_burned:.2f}', (10, 150), font, font_scale, font_color, thickness)
    
    
    return frame

def calculate_calories_burned(exercise_type, counter):
    # MET values for various exercises (example values)
    met_values = {
        'push-up': 3.5,
        'pull-up': 8.0,
        'squat': 5.0,
        'sit-up': 3.0,
        'walk': 3.5,
        'deadlift':4.0
    }
    met = met_values.get(exercise_type, 3.5)  # Default MET if not found
    # Assuming a weight of 70 kg (average adult)
    calories_per_rep = met * 70 / 60 / 10  # Adjust the division factor for realistic values
    return calories_per_rep * counter

def provide_feedback(landmarks, exercise_type):
    feedback = ""

    if exercise_type == "push-up":
        left_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
        left_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
        left_wrist = detection_body_part(landmarks, "LEFT_WRIST")

        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        if elbow_angle > 90:
            feedback += "Keep your elbows closer to your body. "
        if landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y > landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y:
            feedback += "Ensure your back is straight. "
        if landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y < landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y:
            feedback += "Lower your body more. "

    elif exercise_type == "pull-up":
        left_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
        left_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
        left_wrist = detection_body_part(landmarks, "LEFT_WRIST")

        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        if elbow_angle < 90:
            feedback += "Avoid dropping your elbows too low. "
        if landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y < landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y:
            feedback += "Keep your shoulders engaged. "

    elif exercise_type == "squat":
        left_knee = detection_body_part(landmarks, "LEFT_KNEE")
        left_ankle = detection_body_part(landmarks, "LEFT_ANKLE")
        hip = detection_body_part(landmarks, "LEFT_HIP")

        knee_angle = calculate_angle(hip, left_knee, left_ankle)

        if knee_angle < 90:
            feedback += "Ensure your knees don't extend beyond your toes. "
        if landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y > landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y:
            feedback += "Lower your hips more. "

    elif exercise_type == "sit-up":
        left_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
        left_hip = detection_body_part(landmarks, "LEFT_HIP")
        left_knee = detection_body_part(landmarks, "LEFT_KNEE")

        shoulder_angle = calculate_angle(left_hip, left_shoulder, left_knee)

        if shoulder_angle > 90:
            feedback += "Avoid pulling on your neck. Use your core to lift your body. "

    elif exercise_type == "walk":
        # Walking might require checking hip and shoulder positions
        left_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
        left_hip = detection_body_part(landmarks, "LEFT_HIP")

        if left_hip[1] > left_shoulder[1]:
            feedback += "Keep your posture upright while walking. "
            
    
    return feedback

    

from moviepy.editor import ImageSequenceClip

def create_instagram_reel(flagged_frames):
    if not flagged_frames:
        return None  # No frames to process for the reel

    # Ensure the output directory exists
    output_dir = "output/processed_videos/"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "instagram_reel.mp4")

    # Create a video clip from the flagged frames
    clip = ImageSequenceClip(flagged_frames, fps=24)
    
    # Write the video file to the specified path
    clip.write_videofile(output_path, codec="libx264", fps=24)
    
    return output_path