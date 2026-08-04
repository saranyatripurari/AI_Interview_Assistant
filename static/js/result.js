// ============================================================
// result.js — AI Interview Assistant
// Score gauge animation — modal removed (inline Yes/No now)
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const scoreValueEl    = document.getElementById("scoreValue");
    const scoreProgressEl = document.getElementById("scoreProgress");
    const scoreLabelEl    = document.getElementById("scoreLabel");

    if (scoreValueEl) {
        const finalScore = parseInt(scoreValueEl.textContent.trim()) || 0;
        let currentScore = 0;

        const duration   = 1200; // ms
        const steps      = 50;
        const increment  = finalScore / steps;
        const intervalMs = duration / steps;

        // SVG circle perimeter for r=70 is 2 * PI * 70 ≈ 440
        const circumference = 440;

        const timer = setInterval(() => {
            currentScore = Math.min(currentScore + increment, finalScore);
            scoreValueEl.textContent = Math.round(currentScore);

            // Update gauge offset
            if (scoreProgressEl) {
                const offset = circumference - (currentScore / 100) * circumference;
                scoreProgressEl.style.strokeDashoffset = offset;
            }

            if (Math.round(currentScore) >= finalScore) {
                clearInterval(timer);
                scoreValueEl.textContent = finalScore;

                if (scoreProgressEl) {
                    const finalOffset = circumference - (finalScore / 100) * circumference;
                    scoreProgressEl.style.strokeDashoffset = finalOffset;
                }

                updateScoreLabel(finalScore);
            }
        }, intervalMs);
    }

    function updateScoreLabel(score) {
        if (!scoreLabelEl) return;

        if (score >= 80) {
            scoreLabelEl.textContent = "Excellent Performance";
        } else if (score >= 65) {
            scoreLabelEl.textContent = "Good Performance";
        } else if (score >= 50) {
            scoreLabelEl.textContent = "Average Performance";
        } else {
            scoreLabelEl.textContent = "Needs More Practice";
        }
    }

    console.log("✅ AI Interview Assistant — Results JS initialized.");

});