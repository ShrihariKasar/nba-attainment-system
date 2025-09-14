document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector("input[type='file']");
    const uploadForm = document.querySelector("form");

    uploadForm.addEventListener("submit", function (event) {
        const file = fileInput.files[0];

        // Check if a file is selected
        if (!file) {
            showAlert("Please select a file before uploading.", "error");
            event.preventDefault(); // Stop form submission
            return;
        }

        // Check if the file is an Excel file
        if (!file.name.endsWith(".xlsx")) {
            showAlert("Invalid file format. Please upload an Excel (.xlsx) file.", "error");
            event.preventDefault();
            return;
        }

        // Show success message
        showAlert("File uploaded successfully! Processing...", "success");

        // Show a loading indicator (optional)
        showLoader();
    });

    // Function to display alerts dynamically
    function showAlert(message, type) {
        const alertDiv = document.createElement("div");
        alertDiv.className = `flash-message ${type}`;
        alertDiv.textContent = message;
        document.body.prepend(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    // Function to show a loading animation (optional)
    function showLoader() {
        const loader = document.createElement("div");
        loader.className = "loader";
        loader.innerHTML = '<div class="spinner"></div><p>Processing...</p>';
        document.body.appendChild(loader);
    }
});