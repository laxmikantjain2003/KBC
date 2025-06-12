// timer logic
// Enhanced timer logic with accessibility, input disabling, and robust handling
let timer;
let timeLeft = 30; // seconds per question
const timerDisplay = document.getElementById("timer");
const questionForm = document.getElementById("questionForm");

// Function to start the countdown timer
function startTimer() {
    timeLeft = 30; // Reset timer for each new question
    updateTimerDisplay();
    timerDisplay.style.color = ""; // Reset color on new question

    timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();

        // Change timer color to red to warn when 5 seconds or less remain
        if (timeLeft <= 5) {
            timerDisplay.style.color = "red";
        }

        if (timeLeft <= 0) {
            clearInterval(timer);
            autoSubmit();
        }
    }, 1000);
}

// Update the timer display text with aria-live for screen readers
function updateTimerDisplay() {
    timerDisplay.textContent = `⏳ Time Left: ${timeLeft}s`;
    timerDisplay.setAttribute("aria-live", "polite");
}

// Automatically submit the question form when time expires
function autoSubmit() {
    const options = document.querySelectorAll('input[name="answer"]');
    if (options.length > 0) {
        // Disable inputs to prevent changes after time ends
        options.forEach(option => option.disabled = true);

        alert("⏰ Time's up! Your answer will be submitted.");
        if (questionForm) {
            questionForm.submit();
        }
    }
}

// Reset the timer (useful for next question)
function resetTimer() {
    clearInterval(timer);
    startTimer();
}

// Start timer on page load if timer and form exist
window.onload = () => {
    if (timerDisplay && questionForm) {
        startTimer();
    }
};

