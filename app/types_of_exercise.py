import numpy as np
from body_part_angle import BodyPartAngle
from utils import detection_body_part

class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        """
        Initialize the TypeOfExercise class with landmarks.

        Args:
            landmarks: List of pose landmarks detected by Mediapipe.
        """
        super().__init__(landmarks)
        self.landmarks = landmarks  # Store landmarks for use in methods

    def push_up(self, counter, status):
        """Count push-ups based on arm angles."""
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) / 2

        if status:
            if avg_arm_angle < 70:  # Threshold for push-up
                counter += 1
                status = False
        else:
            if avg_arm_angle > 160:
                status = True

        return counter, status

    def pull_up(self, counter, status):
        """Count pull-ups based on nose and shoulder height."""
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        
        if left_elbow[2] < 0.5 or right_elbow[2] < 0.5 or nose[2] < 0.5:  # Ensure visibility
            return counter, status

        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:  # Threshold for pull-up
                counter += 1
                status = False
        else:
            if nose[1] < avg_shoulder_y:
                status = True

        return counter, status

    def squat(self, counter, status):
        """Count squats based on leg angles."""
        left_leg_angle = self.angle_of_the_left_leg()
        right_leg_angle = self.angle_of_the_right_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) / 2

        if status:
            if avg_leg_angle < 70:  # Threshold for squat
                counter += 1
                status = False
        else:
            if avg_leg_angle > 160:
                status = True

        return counter, status

    def walk(self, counter, status):
        """Count walking steps based on knee positions."""
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")

        if left_knee[2] < 0.5 or right_knee[2] < 0.5:  # Ensure visibility
            return counter, status

        if status:
            if left_knee[0] > right_knee[0]:  # Threshold for step
                counter += 1
                status = False
        else:
            if left_knee[0] < right_knee[0]:
                counter += 1
                status = True

        return counter, status

    def sit_up(self, counter, status):
        """Count sit-ups based on abdominal angle."""
        angle = self.angle_of_the_abdomen()
        
        if status:
            if angle < 55:  # Threshold for sit-up
                counter += 1
                status = False
        else:
            if angle > 105:
                status = True

        return counter, status
    

    def calculate_exercise(self, exercise_type, counter, status):
        """Calculate the count and status for the specified exercise."""
        if exercise_type == "push-up":
            counter, status = self.push_up(counter, status)
        elif exercise_type == "pull-up":
            counter, status = self.pull_up(counter, status)
        elif exercise_type == "squat":
            counter, status = self.squat(counter, status)
        elif exercise_type == "walk":
            counter, status = self.walk(counter, status)
        elif exercise_type == "sit-up":
            counter, status = self.sit_up(counter, status)

        return counter, status
