// ============================================================
// feature_detail.js — AI Interview Assistant
// Shared interactivity for all feature detail pages
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    // ===============================
    // Navbar Scroll Effect
    // ===============================
    const navbar = document.getElementById("navbar");

    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 40) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        }, { passive: true });
    }

    // ===============================
    // Mobile Menu Toggle
    // ===============================
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const nav = document.querySelector(".navbar nav");

    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener("click", () => {
            const isOpen = nav.style.display === "flex";
            if (isOpen) {
                nav.style.display = "none";
            } else {
                nav.style.display = "flex";
                nav.style.flexDirection = "column";
                nav.style.position = "absolute";
                nav.style.top = "72px";
                nav.style.left = "0";
                nav.style.width = "100%";
                nav.style.background = "#FFFFFF";
                nav.style.padding = "24px";
                nav.style.gap = "16px";
                nav.style.borderBottom = "1px solid #E5E7EB";
                nav.style.boxShadow = "0 10px 30px rgba(0,0,0,0.06)";
                nav.style.zIndex = "999";
            }
        });

        nav.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                if (window.innerWidth < 768) {
                    nav.style.display = "none";
                }
            });
        });
    }

    // ===============================
    // Step Reveal (How It Works)
    // ===============================
    const steps = document.querySelectorAll(".step-item");

    if (steps.length) {
        const stepObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add("step-visible");
                    }, i * 120);
                    stepObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: "0px 0px -30px 0px" });

        steps.forEach(step => stepObserver.observe(step));
    }

    // ===============================
    // Benefit Card Reveal
    // ===============================
    const benefitCards = document.querySelectorAll(".benefit-card");

    if (benefitCards.length) {
        const cardObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = "1";
                        entry.target.style.transform = "translateY(0)";
                    }, i * 80);
                    cardObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

        benefitCards.forEach(card => {
            card.style.opacity = "0";
            card.style.transform = "translateY(16px)";
            card.style.transition = "opacity 0.45s ease, transform 0.45s ease";
            cardObserver.observe(card);
        });
    }

    // ===============================
    // Back Link / Home Button — smooth page exit
    // ===============================
    document.querySelectorAll(".back-link, .fd-back-home-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const targetUrl = btn.getAttribute("href") || "/";
            document.body.style.opacity = "0";
            document.body.style.transform = "translateY(-8px)";
            document.body.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            setTimeout(() => {
                window.location.href = targetUrl;
            }, 280);
        });
    });

    console.log("✅ AI Interview Assistant — Feature Detail JS initialized.");
});
