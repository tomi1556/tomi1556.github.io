document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader (オープニングアニメーション) =====
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        // アニメーションのシーケンスを開始
        setTimeout(() => {
            preloader.classList.add('start-animation');
        }, 500);

        // サイト表示への切り替え
        setTimeout(() => {
            preloader.classList.add('hidden');
            initHeroTextAnimation();
        }, 2800); // この時間はCSSのアニメーション時間と調整
    } else {
        // プリローダーがない場合は直接ヒーローアニメーションを開始
        initHeroTextAnimation();
    }

    // ===== Header & Navigation (ヘッダーとナビゲーション) =====
    const header = document.querySelector('header');
    const hamburger = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('.main-nav');

    // スクロール時のヘッダースタイル変更
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    // ハンバーガーメニューの動作
    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            const isActive = hamburger.classList.toggle('active');
            nav.classList.toggle('active', isActive);
            document.body.classList.toggle('no-scroll', isActive);
            hamburger.setAttribute('aria-expanded', isActive.toString());
        });

        // メニュー項目クリックでメニューを閉じる
        nav.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                // 通常のナビゲーションを妨げないように
                if (nav.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    nav.classList.remove('active');
                    document.body.classList.remove('no-scroll');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    // ===== Hero Text Animation (ヒーローテキストのアニメーション) =====
    function initHeroTextAnimation() {
        const setupAnimation = (elementSelector, baseDelay) => {
            const element = document.querySelector(elementSelector);
            if (!element) return;

            const text = element.innerHTML.replace(/<br\s*\/?>/gi, ' \n ').trim(); // 改行を保持
            element.innerHTML = '';
            
            text.split('').forEach(char => {
                if (char === '\n') {
                    element.appendChild(document.createElement('br'));
                } else {
                    const span = document.createElement('span');
                    span.innerHTML = (char === ' ') ? '&nbsp;' : char;
                    element.appendChild(span);
                }
            });

            setTimeout(() => {
                element.classList.add('visible');
                element.querySelectorAll('span').forEach((span, index) => {
                    span.style.transitionDelay = `${index * 0.04}s`;
                });
            }, baseDelay);
        };

        setupAnimation('.animate-title', 200);
        setupAnimation('.animate-subtitle', 600);
    }

    // ===== Footer Year (フッターの年号) =====
    const currentYearEl = document.getElementById('current-year');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear().toString();
    }

    // ===== Clipboard.js (コピー機能) =====
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

            clipboard.on('error', (e) => {
                toast.textContent = 'コピーに失敗しました';
                toast.className = 'copy-toast show error';
                setTimeout(() => { toast.className = 'copy-toast'; }, 2000);
            });
        }
    }

    // ===== Scroll Animations (スクロール時のアニメーション) =====
    const animatedElements = document.querySelectorAll('.animate-on-scroll, .animate-on-load');
    if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observerInstance) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const animationDelay = el.dataset.animationDelay || '0s';
                    el.style.transitionDelay = animationDelay;
                    el.classList.add('is-visible');
                    observerInstance.unobserve(el);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(el => observer.observe(el));
    }
});
