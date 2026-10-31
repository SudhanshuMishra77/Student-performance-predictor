import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# STEP 1: Generate sample student data
np.random.seed(42)

number_of_students = 500

study_hours = np.random.uniform(0, 10, number_of_students)
attendance = np.random.uniform(40, 100, number_of_students)
previous_marks = np.random.uniform(30, 100, number_of_students)

# Demo formula to create sample final marks
noise = np.random.normal(0, 5, number_of_students)

final_score = (
    3 * study_hours
    + 0.2 * attendance
    + 0.5 * previous_marks
    + noise
)

final_score = np.clip(final_score, 0, 100)

# STEP 2: Create the dataset
df = pd.DataFrame({
    "study_hours": study_hours,
    "attendance": attendance,
    "previous_marks": previous_marks,
    "final_score": final_score
})

# Save dataset as CSV
df.to_csv("student_data.csv", index=False)

print("Dataset created successfully!")
print(df.head())

# STEP 3: Separate input features and target
X = df[["study_hours", "attendance", "previous_marks"]]
Y = df["final_score"]

# STEP 4: Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# STEP 5: Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, Y_train)

print("\nModel training completed!")

# STEP 6: Evaluate the model
predictions = model.predict(X_test)

mae = mean_absolute_error(Y_test, predictions)
r2 = r2_score(Y_test, predictions)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")

# STEP 7: Save the trained model
joblib.dump(model, "model.pkl")

print("\nModel saved as model.pkl")

# STEP 8: Test a new student
new_student = pd.DataFrame([{
    "study_hours": 5,
    "attendance": 80,
    "previous_marks": 70
}])

predicted_marks = model.predict(new_student)[0]
predicted_marks = np.clip(predicted_marks, 0, 100)

print(f"\nPredicted final marks: {predicted_marks:.2f}/100")