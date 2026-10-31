import random
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
# Make results reproducible
random.seed(42)
# Generate sample student data
students = []
for _ in range(2000):
    study_hours = round(random.uniform(0, 12), 1)
    previous_score = round(random.uniform(30, 100), 1)
    attendance = round(random.uniform(40, 100), 1)
    sleep_hours = round(random.uniform(3, 10), 1)
    tutoring = random.choice([0, 1])
    # Simulated relationship between student habits and scores
    score = (
        0.45 * previous_score
        + 2.0 * study_hours
        + 0.15 * attendance
        + 1.0 * sleep_hours
        + 3.0 * tutoring
        - 5
        + random.uniform(-5, 5)
    )
    score = max(0, min(100, score))
    students.append({
        "study_hours": study_hours,
        "previous_score": previous_score,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "tutoring": tutoring,
        "final_score": round(score, 2)
    })
# Convert the data into a table
data = pd.DataFrame(students)
# Separate inputs and expected output
X = data[
    [
        "study_hours",
        "previous_score",
        "attendance",
        "sleep_hours",
        "tutoring"
    ]
]
y = data["final_score"]
# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Train the machine-learning model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)
# Evaluate the model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print("Student Performance Model Trained Successfully!")
print(f"Mean Absolute Error: {mae:.2f} points")
# Save the trained model
joblib.dump(model, "student_performance_model.pkl")
print("Model saved as student_performance_model.pkl")