// Buttons
const startBtn = document.getElementById("startBtn");
const startInterview = document.getElementById("startInterview");

// Dropdowns
const role = document.getElementById("role");
const experience = document.getElementById("experience");

// Function
function beginInterview() {

    const selectedRole = role.value;
    const selectedExperience = experience.value;

    // Save selections
    localStorage.setItem("role", selectedRole);
    localStorage.setItem("experience", selectedExperience);

    // Loading Animation
    if (startBtn) {
        startBtn.innerHTML = "⏳ Preparing Interview...";
        startBtn.disabled = true;
    }

    setTimeout(() => {

        window.location.href = "/interview";

    }, 1500);

}

// Events
if (startBtn) {
    startBtn.addEventListener("click", beginInterview);
}

if (startInterview) {
    startInterview.addEventListener("click", beginInterview);
}