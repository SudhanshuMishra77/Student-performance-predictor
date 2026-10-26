import joblib
import pandas as pd
import numpy as np

# Load the saved model
model = joblib.load("model.pkl")


def predict_score(study_hours, attendance, previous_marks):
    # Validate input values
    values = [study_hours, attendance, previous_marks]

    if not all(np.isfinite(v) for v in values):
        raise ValueError("Inputs must be valid numbers.")

    if not 0 <= study_hours <= 24:
        raise ValueError("Study hours must be between 0 and 24.")

    if not 0 <= attendance <= 100:
        raise ValueError("Attendance must be between 0 and 100.")

    if not 0 <= previous_marks <= 100:
        raise ValueError("Previous marks must be between 0 and 100.")

    student = pd.DataFrame([{
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_marks": previous_marks
    }])

    prediction = model.predict(student)[0]

    # Keep the displayed score between 0 and 100
    return round(float(np.clip(prediction, 0, 100)), 2)


# Test the function
if _name_ == "_main_":
    result = predict_score(
        study_hours=5,
        attendance=80,
        previous_marks=70
    )

    print("Predicted marks:", result, "/100")