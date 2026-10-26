document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const resultDiv = document.getElementById("resultContent");

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevents page reload on form submit

    // 1. Gather all 5 form input values matching app.py
    const payload = {
      study_hours: parseFloat(document.getElementById("study_hours").value),
      previous_score: parseFloat(document.getElementById("previous_score").value),
      attendance: parseFloat(document.getElementById("attendance").value),
      sleep_hours: parseFloat(document.getElementById("sleep_hours").value),
      tutoring: document.getElementById("tutoring").value // "yes" or "no" / 1 or 0
    };

    // 2. Show a loading message while waiting for backend
    resultDiv.innerHTML = "<p>Analyzing data and predicting...</p>";

    try {
      // 3. Send POST request to the correct Flask endpoint
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      // 4. Update the DOM dynamically with the result
      if (response.ok) {
        resultDiv.innerHTML = `
          <div class="success-card">
            <h3>Predicted Score: ${data.predicted_score}%</h3>
            <p>Performance Category: <strong>${data.performance_category}</strong></p>
            <p class="text-muted"><small>${data.message}</small></p>
          </div>
        `;
      } else {
        resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
      }
    } catch (error) {
      resultDiv.innerHTML = `<p class="error">Failed to connect to backend server.</p>`;
    }
  });
});