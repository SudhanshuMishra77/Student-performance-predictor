document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const resultDiv = document.getElementById("resultContent");

  // 1. Load history table data when the page first opens
  loadHistory();

  // 2. Handle form submission for predictions
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevents page reload on form submit

    // Gather all 5 form input values matching app.py
    const payload = {
      study_hours: parseFloat(document.getElementById("study_hours").value),
      previous_score: parseFloat(document.getElementById("previous_score").value),
      attendance: parseFloat(document.getElementById("attendance").value),
      sleep_hours: parseFloat(document.getElementById("sleep_hours").value),
      tutoring: document.getElementById("tutoring").value // "1" or "0"
    };

    // Show a loading message while waiting for backend
    resultDiv.innerHTML = "<p>Analyzing data and predicting...</p>";

    try {
      // Send POST request to the correct Flask endpoint
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      // Update the DOM dynamically with the result
      if (response.ok) {
        resultDiv.innerHTML = `
          <div class="success-card">
            <h3>Predicted Score: ${data.predicted_score}%</h3>
            <p>Performance Category: <strong>${data.performance_category}</strong></p>
            <p class="text-muted"><small>${data.message}</small></p>
          </div>
        `;
        
        // Instantly refresh the history table to show this new prediction!
        loadHistory();
      } else {
        resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
      }
    } catch (error) {
      resultDiv.innerHTML = `<p class="error">Failed to connect to backend server.</p>`;
    }
  });
});

// 3. Function to fetch and render prediction history from your Flask backend
async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const data = await response.json();
    const historyData = data.history || []; // Grab the history array safely
    
    const tableBody = document.getElementById("historyTableBody");
    if (!tableBody) return; // Exit if table body isn't on the page
    
    tableBody.innerHTML = ""; // Clear existing rows
    
    if (historyData.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--muted);">No history recorded yet.</td></tr>`;
      return;
    }

    // Loop through records and create table rows dynamically
    historyData.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.created_at || 'Just now'}</td>
        <td>${item.study_hours}</td>
        <td>${item.previous_score}</td>
        <td>${item.attendance}%</td>
        <td>${item.sleep_hours}</td>
        <td>${item.tutoring == 1 ? 'Yes' : 'No'}</td>
        <td><strong>${item.predicted_score}%</strong></td>
        <td><span class="category-badge">${item.performance_category || item.category || 'N/A'}</span></td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Failed to load history:", error);
  }
}