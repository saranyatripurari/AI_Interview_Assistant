// ============================================================
// interview.js — AI Interview Assistant
// Vertical scroll layout: timer, progress tracking, localStorage
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const form          = document.getElementById("interviewForm");
    const textareas     = document.querySelectorAll("textarea");
    const progressFill  = document.getElementById("progress");
    const progressText  = document.getElementById("progressText");
    const timerDisplay  = document.getElementById("timer");
    const timerBox      = document.getElementById("timerBox");
    const loadingScreen = document.getElementById("loading");

    const totalQuestions = textareas.length;

    // =========================================================
    // Progress Tracking — count filled textareas
    // =========================================================

    function updateProgress() {
        let answered = 0;
        textareas.forEach(area => {
            if (area.value.trim().length > 0) answered++;
        });
        const pct = totalQuestions > 0
            ? Math.round((answered / totalQuestions) * 100)
            : 0;
        if (progressFill) progressFill.style.width = pct + "%";
        if (progressText) progressText.textContent = `${pct}% Answered`;
    }

    // =========================================================
    // Word Count + localStorage Auto-Save per textarea
    // =========================================================

    textareas.forEach((area, idx) => {
        const storageKey = "iv_answer_" + idx;
        const wcEl       = document.getElementById("wc-" + idx);

        // Restore saved draft
        const saved = localStorage.getItem(storageKey);
        if (saved !== null) {
            area.value = saved;
        }

        function updateWordCount() {
            const text  = area.value.trim();
            const words = text ? text.split(/\s+/).length : 0;
            if (wcEl) {
                wcEl.textContent = `${words} word${words === 1 ? "" : "s"}`;
            }
        }

        updateWordCount();

        area.addEventListener("input", () => {
            localStorage.setItem(storageKey, area.value);
            updateWordCount();
            updateProgress();
        });
    });

    // Run initial progress calculation (in case drafts were restored)
    updateProgress();

    // =========================================================
    // Countdown Timer — 30 minutes
    // =========================================================

    let remainingTime = 30 * 60; // 1800 seconds

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    }

    if (timerDisplay) timerDisplay.textContent = formatTime(remainingTime);

    const timerInterval = setInterval(() => {
        remainingTime--;

        if (timerDisplay) timerDisplay.textContent = formatTime(remainingTime);

        // Warning state at 5 minutes
        if (remainingTime <= 300 && timerBox) {
            timerBox.classList.add("timer-warning");
        }

        // Auto-submit on timeout
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            if (loadingScreen) loadingScreen.style.display = "flex";
            if (form) form.submit();
        }
    }, 1000);

    // =========================================================
    // Form Submit — Interactive validation & loading overlay
    // =========================================================

    if (form) {
        form.addEventListener("submit", (e) => {
            let answeredCount = 0;
            textareas.forEach(area => {
                if (area.value.trim().length > 0) answeredCount++;
            });

            if (answeredCount === 0) {
                const proceed = confirm("You haven't answered any questions yet.\n\nClick 'OK' to submit anyway, or 'Cancel' to stay and provide valid answers.");
                if (!proceed) {
                    e.preventDefault();
                    if (textareas[0]) textareas[0].focus();
                    return;
                }
            }

            // Show loading overlay immediately
            if (loadingScreen) loadingScreen.style.display = "flex";

            // Clear saved drafts
            for (let i = 0; i < totalQuestions; i++) {
                localStorage.removeItem("iv_answer_" + i);
            }
        });
    }

    console.log("✅ Interview Assistant — vertical scroll JS loaded.");
});