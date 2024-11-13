import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

class ProgressPredictor:
    def __init__(self, metrics_file):
        self.metrics_file = metrics_file
        self.model = None
        self.load_model()  # Try to load an existing model

    def load_model(self):
        if os.path.exists('model.pkl'):
            self.model = joblib.load('model.pkl')
        else:
            self.model = LinearRegression()  # Default to a new model if none exists

    def train_model(self):
        metrics_df = pd.read_csv(self.metrics_file)
        X = metrics_df[['Exercise Counts', 'Calories Burned']]
        y = metrics_df['Weight (kg)']
        self.model.fit(X, y)
        joblib.dump(self.model, 'model.pkl')  # Save the trained model

    def predict_future(self, exercise_counts, calories_burned):
        future_weight = self.model.predict(np.array([[exercise_counts, calories_burned]]))
        return future_weight[0]
