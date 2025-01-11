const onButton = document.getElementById('onButton');
const offButton = document.getElementById('offButton');
const status = document.getElementById('status');

// Function to handle turning ON the detection mode
function startDetection() {
    fetch('http://127.0.0.1:5001/start-detection')  // Ensure this URL is correct
        .then(response => response.json())
        .then(data => {
            if (data.message === "Detection started!") {
                status.innerHTML = "<p>Detection Mode is ON</p>";
                onButton.disabled = true;
                offButton.disabled = false;
            }
        })
        .catch((error) => {
            console.error('Error:', error);  // Log any errors
        });
}

// Function to handle turning OFF the detection mode
function stopDetection() {
    fetch('http://127.0.0.1:5001/stop-detection')
        .then(response => response.json())
        .then(data => {
            if (data.message === "Detection stopped!") {
                status.innerHTML = "<p>Detection Mode is OFF</p>";
                onButton.disabled = false;
                offButton.disabled = true;
            }
        })
        .catch((error) => {
            console.error('Error:', error);  // Log any errors
        });
}

// Attach event listeners to buttons
onButton.addEventListener('click', startDetection);
offButton.addEventListener('click', stopDetection);
