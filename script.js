document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader (オープニングアニメーション) =====
    const body = document.body;
    const preloader = document.querySelector('.preloader');

    if (preloader) {
        // ページが完全に読み込まれたらアニメーションを開始
        window.addEventListener('load', () => {
            setTimeout(() => {
                body.classList.remove('is-loading');
                preloader.classList.add('hidden');
                initHeroTextAnimation();
            }, 500); 
        });
    } else {
        // プリローダーがない場合は直接表示
        body.classList.remove('is-loading');
        initHeroTextAnimation();
    }


    // ===== Header & Navigation (ヘッダーとナビゲーション) =====
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

    // ===== Hero Text Animation (ヒーローテキストのアニメーション) =====
    function initHeroTextAnimation() {
        const titleElement = document.getElementById('typing-title');
        const subtitleElement = document.getElementById('typing-subtitle');
        
        if (titleElement) titleElement.innerHTML = '';
        if (subtitleElement) subtitleElement.innerHTML = '';
        
        if (titleElement) {
            typewriter(titleElement, "StellaMC", 150, () => {
                loopingTypingEffect();
            });
        }
    }

    // 汎用タイピング関数
    function typewriter(element, text, speed, callback) {
        let charIndex = 0;
        element.classList.add('typing-cursor');

        function type() {
            if (charIndex < text.length) {
                element.textContent += text.charAt(charIndex);
                charIndex++;
                setTimeout(type, speed + (Math.random() * 40 - 20));
            } else {
                element.classList.remove('typing-cursor');
                if (callback) callback();
            }
        }
        type();
    }

    // サブタイトルのループタイピング関数
    function loopingTypingEffect() {
        const subtitleElement = document.getElementById('typing-subtitle');
        if (!subtitleElement) return;

        const texts = [
            "安心できるからこそ、本気で楽しめる。",
            "心安らぐ、あなたのもう一つの居場所。",
            "民度最優先。",
            "最高のMinecraftサーバー！"
        ];
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typeSpeed = 120;
        const deleteSpeed = 60;
        const pauseEnd = 2200;

        function loop() {
            subtitleElement.classList.add('blinking-cursor');
            
            setTimeout(() => {
                subtitleElement.classList.remove('blinking-cursor');
                subtitleElement.classList.add('typing-cursor');
                typeDelete();
            }, 500);
        }

        function typeDelete() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                // 削除
                subtitleElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                if (charIndex === 0) {
                    isDeleting = false;
                    textIndex = (textIndex + 1) % texts.length;
                    subtitleElement.classList.remove('typing-cursor');
                    subtitleElement.classList.add('blinking-cursor');
                    setTimeout(loop, 500);
                } else {
                    setTimeout(typeDelete, deleteSpeed);
                }
            } else {
                // 入力
                subtitleElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                if (charIndex === currentText.length) {
                    isDeleting = true;
                    subtitleElement.classList.remove('typing-cursor');
                    subtitleElement.classList.add('blinking-cursor');
                    setTimeout(typeDelete, pauseEnd);
                } else {
                    setTimeout(typeDelete, typeSpeed);
                }
            }
        }
        setTimeout(loop, 1000);
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
                toast.textContent = `${e.trigger.ariaLabel.replace('をコピー', '')} をコピーしました！`;
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
        }, { threshold: 0.15 });

        animatedElements.forEach(el => observer.observe(el));
    }
});
