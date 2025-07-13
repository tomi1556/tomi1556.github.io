document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader =====
    const preloader = document.querySelector('.preloader');
    window.addEventListener('load', () => {
        setTimeout(() => {
            preloader.classList.add('hidden');
        }, 300); // 300ms待ってから非表示
    });

    // ===== Header & Navigation =====
    const header = document.querySelector('header');
    const hamburger = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('.main-nav');

    // Scroll-based header style
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Hamburger menu toggle
    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            const isActive = hamburger.classList.toggle('active');
            nav.classList.toggle('active', isActive);
            document.body.classList.toggle('no-scroll', isActive);
            hamburger.setAttribute('aria-expanded', isActive);
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

    // ===== Hero Parallax Effect =====
    const heroBg = document.querySelector('.hero-background-image');
    if (heroBg) {
        window.addEventListener('scroll', () => {
            const offset = window.pageYOffset;
            heroBg.style.transform = `translateY(${offset * 0.25}px) scale(1.1)`;
        });
    }
    
    // ===== Footer Year =====
    const currentYearEl = document.getElementById('current-year');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
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
                setTimeout(() => {
                    toast.className = 'copy-toast';
                }, 2000);
                e.clearSelection();
            });

            clipboard.on('error', () => {
                toast.textContent = 'コピーに失敗しました';
                toast.className = 'copy-toast show';
                setTimeout(() => {
                    toast.className = 'copy-toast';
                }, 2000);
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
                    const animationType = el.dataset.animation || 'fadeInUpCustom';
                    const animationDelay = el.dataset.animationDelay || '0s';
                    el.style.animationDelay = animationDelay;
                    el.classList.add(animationType, 'is-visible');
                    observerInstance.unobserve(el);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }
});
