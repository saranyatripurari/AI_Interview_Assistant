// ============================================================
// landing.js — AI Interview Assistant
// Modern SaaS Landing Page Interactivity
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
    // Smooth Scroll for Nav Links
    // ===============================
    document.querySelectorAll("a[href^='#']").forEach(link => {
        link.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (!href || href === "#") return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const navHeight = navbar ? navbar.offsetHeight : 72;
                const top = target.getBoundingClientRect().top + window.scrollY - navHeight;

                window.scrollTo({
                    top: top,
                    behavior: "smooth"
                });
            }
        });
    });


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

        // Close menu on link click
        nav.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                if (window.innerWidth < 768) {
                    nav.style.display = "none";
                }
            });
        });
    }


    // ===============================
    // Scroll Reveal (data-aos)
    // ===============================
    function setupScrollReveal() {
        const elements = document.querySelectorAll("[data-aos]");
        if (!elements.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add("aos-animate");
                    }, i * 60);

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: "0px 0px -40px 0px"
        });

        elements.forEach(el => observer.observe(el));
    }

    setupScrollReveal();


    // ===============================
    // Start Interview Button Loading State
    // ===============================
    const startForm = document.getElementById("startForm");
    const startBtn = document.getElementById("startBtn");

    if (startForm && startBtn) {
        startForm.addEventListener("submit", () => {
            startBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2.5" stroke-linecap="round"
                     style="animation: spin 0.8s linear infinite; display:inline-block; margin-right:8px;">
                    <line x1="12" y1="2" x2="12" y2="6"/>
                    <line x1="12" y1="18" x2="12" y2="22"/>
                    <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/>
                    <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/>
                    <line x1="2" y1="12" x2="6" y2="12"/>
                    <line x1="18" y1="12" x2="22" y2="12"/>
                </svg>
                Generating Session...
            `;
            startBtn.disabled = true;
            startBtn.style.opacity = "0.85";
            startBtn.style.cursor = "not-allowed";

            if (!document.getElementById("spinStyle")) {
                const style = document.createElement("style");
                style.id = "spinStyle";
                style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
                document.head.appendChild(style);
            }
        });
    }

    console.log("✅ AI Interview Assistant — Landing JS initialized.");

});