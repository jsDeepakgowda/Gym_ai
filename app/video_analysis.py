import cv2
import mediapipe as mp
from types_of_exercise import TypeOfExercise
from utils import score_table, calculate_calories_burned, provide_feedback, create_instagram_reel
import os

class VideoAnalysis:
    def __init__(self, video_path=None):
        self.video_path = video_path
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.calories_burned = 0.0  # Initialize calories burned
        self.counter = 0  # Initialize exercise counter
        self.flagged_frames = []  # Store frames with feedback issues for reel compilation
        self.screenshot_dir = "output/screenshots/"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.feedback = ""  # Initialize feedback attribute

    def analyze_video(self, exercise_type, stop_analysis_func=None):
        """Generator function to analyze video frames for the specified exercise."""
        cap = cv2.VideoCapture(self.video_path or 0)  # Use webcam if no video path provided
        status = True

        with self.mp_pose.Pose(
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7,
                model_complexity=2
        ) as pose:
            while cap.isOpened():
                # Check if the stop function was called (Stop analysis)
                if stop_analysis_func and stop_analysis_func():  # Check if stop was triggered
                    break  # Stop analysis

                ret, frame = cap.read()
                if not ret:
                    break

                # Resize and convert frame for analysis
                frame = cv2.resize(frame, (1280, 720))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    exercise = TypeOfExercise(landmarks)
                    self.counter, status = exercise.calculate_exercise(exercise_type, self.counter, status)

                    # Draw landmarks
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=3, circle_radius=3),
                        self.mp_drawing.DrawingSpec(color=(174, 139, 45), thickness=2, circle_radius=2)
                    )

                    # Calculate calories burned based on exercise count
                    self.calories_burned = calculate_calories_burned(exercise_type, self.counter)

                    # Provide feedback based on current landmarks
                    self.feedback = provide_feedback(landmarks, exercise_type)  # Store feedback in attribute

                    # If feedback is flagged, save frame and timestamp
                    if self.feedback and len(self.flagged_frames) < 10:  # Limit to 10 flagged frames
                        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
                        screenshot_path = f"{self.screenshot_dir}screenshot_{int(timestamp)}.png"
                        cv2.imwrite(screenshot_path, frame)
                        self.flagged_frames.append(frame)  # Save flagged frame for reel

                    # Overlay exercise info on the frame
                    frame = score_table(exercise_type, frame, self.counter, status, self.calories_burned, self.feedback)

                # Yield the processed frame for real-time display
                yield frame  # Use a generator to return frames one at a time

        cap.release()
        cv2.destroyAllWindows()  # Close the video window

        # If flagged frames exist, create an Instagram reel
        if self.flagged_frames:
            reel_path = create_instagram_reel(self.flagged_frames)
            if reel_path:
                print(f"Reel created at: {reel_path}")
            else:
                print("Error: Unable to create the Instagram Reel.")
        else:
            print("No feedback frames flagged; no Instagram Reel created.")

    def get_summary(self):
        """Returns total calories burned, total count of exercises performed, and final feedback."""
        return self.calories_burned, self.counter

    def get_current_progress(self):
        """Returns current reps, calories burned, and feedback for real-time progress tracking."""
        return {
            "current_reps": self.counter,
            "current_calories": self.calories_burned,
            "feedback": self.feedback
        }
