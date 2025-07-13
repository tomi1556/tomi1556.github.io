document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader =====
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('hidden');
                initHeroTextAnimation();
            }, 200);
        });
    } else {
        initHeroTextAnimation();
    }

    // ===== Header & Navigation =====
    const header = document.querySelector('header');
    const hamburger = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('.main-nav');

    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            const isActive = hamburger.classList.toggle('active');
            nav.classList.toggle('active', isActive);
            document.body.classList.toggle('no-scroll', isActive);
            hamburger.setAttribute('aria-expanded', isActive.toString());
        });

        nav.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (nav.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    nav.classList.remove('active');
                    document.body.classList.remove('no-scroll');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    // ===== Hero Text Animation =====
    function initHeroTextAnimation() {
        const setupAnimation = (element, baseDelay) => {
            if (!element) return;
            const text = element.textContent.trim();
            element.innerHTML = '';
            text.split('').forEach(char => {
                const span = document.createElement('span');
                span.textContent = char === ' ' ? '\u00A0' : char; // Handle spaces
                element.appendChild(span);
            });

            setTimeout(() => {
                element.classList.add('visible');
                element.querySelectorAll('span').forEach((span, index) => {
                    span.style.transitionDelay = `${index * 0.05}s`;
                });
            }, baseDelay);
        };
        
        setupAnimation(document.querySelector('.animate-title'), 200);
        setupAnimation(document.querySelector('.animate-subtitle'), 600);
    }

    // ===== Footer Year =====
    const currentYearEl = document.getElementById('current-year');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear().toString();
    }

    // ===== Clipboard.js =====
    if (typeof ClipboardJS !== 'undefined') {
        const clipboard = new ClipboardJS('.copy-action-btn');
        const toast = document.getElementById('copy-toast');
        if (toast) {
            clipboard.on('success', (e) => {
                const label = e.trigger.getAttribute('aria-label') || 'コンテンツ';
                toast.textContent = `${label.replace('をコピー', '')} をコピーしました！`;
                toast.className = 'copy-toast show';
                setTimeout(() => { toast.className = 'copy-toast'; }, 2000);
                e.clearSelection();
            });

            clipboard.on('error', () => {
                toast.textContent = 'コピーに失敗しました';
                toast.className = 'copy-toast show';
                setTimeout(() => { toast.className = 'copy-toast'; }, 2000);
            });
        }
    }

    // ===== Scroll Animations (Intersection Observer) =====
    const animatedElements = document.querySelectorAll('.animate-on-scroll, .animate-on-load');
    if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observerInstance) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const animationName = el.dataset.animation || 'slideInUp';
                    const animationDelay = el.dataset.animationDelay || '0s';
                    
                    el.style.animationName = animationName;
                    el.style.animationDelay = animationDelay;
                    el.classList.add('is-visible');

                    observerInstance.unobserve(el);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(el => observer.observe(el));
    }
});
