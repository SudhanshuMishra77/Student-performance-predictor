document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const resultDiv = document.getElementById("result");

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevents page reload on form submit

    // 1. Gather form input values
    const payload = {
      study_hours: parseFloat(document.getElementById("study_hours").value),
      attendance: parseFloat(document.getElementById("attendance").value),
      previous_marks: parseFloat(document.getElementById("previous_marks").value)
    };

    // 2. Show a loading message while waiting for backend
    resultDiv.innerHTML = "<p>Analyzing data and predicting...</p>";

    try {
      // 3. Send POST request to Flask endpoint
      const response = await fetch("/predict", {
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
            <p>Status: ${data.status_message}</p>
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