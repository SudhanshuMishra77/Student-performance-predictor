import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the trained prediction model
MODEL_PATH = "student_performance_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model file not found. Run: python train_model.py"
    )

model = joblib.load(MODEL_PATH)

# Database for saving prediction history
DATABASE_PATH = "predictions.db"


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                study_hours REAL NOT NULL,
                previous_score REAL NOT NULL,
                attendance REAL NOT NULL,
                sleep_hours REAL NOT NULL,
                tutoring INTEGER NOT NULL,
                predicted_score REAL NOT NULL,
                performance_category TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


init_db()

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# API route for predicting student performance
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Please send JSON data."}), 400

    required_fields = [
        "study_hours",
        "previous_score",
        "attendance",
        "sleep_hours",
        "tutoring"
    ]

    # Check that all fields are present
    missing = [
        field for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": "Missing fields",
            "fields": missing
        }), 400

    try:
        study_hours = float(data["study_hours"])
        previous_score = float(data["previous_score"])
        attendance = float(data["attendance"])
        sleep_hours = float(data["sleep_hours"])

        tutoring_value = data["tutoring"]

        if tutoring_value in (True, 1, "1", "yes", "Yes"):
            tutoring = 1
        elif tutoring_value in (False, 0, "0", "no", "No"):
            tutoring = 0
        else:
            return jsonify({
                "error": "Tutoring must be yes or no."
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Enter valid numeric values for student details."
        }), 400

    # Validate the input ranges
    if not 0 <= study_hours <= 24:
        return jsonify({
            "error": "Study hours must be between 0 and 24."
        }), 400

    if not 0 <= previous_score <= 100:
        return jsonify({
            "error": "Previous score must be between 0 and 100."
        }), 400

    if not 0 <= attendance <= 100:
        return jsonify({
            "error": "Attendance must be between 0 and 100."
        }), 400

    if not 0 <= sleep_hours <= 24:
        return jsonify({
            "error": "Sleep hours must be between 0 and 24."
        }), 400

    # Arrange inputs in the same format used during training
    student = pd.DataFrame([{
        "study_hours": study_hours,
        "previous_score": previous_score,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "tutoring": tutoring
    }])

    # Generate the predicted score
    predicted_score = float(model.predict(student)[0])
    predicted_score = round(
        max(0, min(100, predicted_score)), 2
    )

    # Assign a simple performance category
    if predicted_score >= 85:
        category = "Excellent"
    elif predicted_score >= 70:
        category = "Good"
    elif predicted_score >= 50:
        category = "Average"
    else:
        category = "Needs Improvement"
    # Save this prediction in the database
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.execute("""
            INSERT INTO predictions (
                created_at,
                study_hours,
                previous_score,
                attendance,
                sleep_hours,
                tutoring,
                predicted_score,
                performance_category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            study_hours,
            previous_score,
            attendance,
            sleep_hours,
            tutoring,
            predicted_score,
            category
        ))

        conn.commit()
    finally:
        conn.close()

    return jsonify({
        "predicted_score": predicted_score,
        "performance_category": category,
        "message": (
            "This is an estimate from a demonstration model, "
            "not a guaranteed exam result."
        )
    })

# API to retrieve recent predictions
@app.route("/api/history", methods=["GET"])
def prediction_history():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute("""
            SELECT *
            FROM predictions
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()
    finally:
        conn.close()

    return jsonify({
        "history": [dict(row) for row in rows]
    })

if __name__ == "__main__":
    app.run(debug=True)