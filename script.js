document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader (オープニングアニメーション) =====
    const body = document.body;
    const preloader = document.querySelector('.preloader');
    const preloaderContainer = document.querySelector('.preloader-container');

    if (preloader) {
        setTimeout(() => {
            if(preloaderContainer) preloaderContainer.classList.add('animated');
        }, 1200);

        setTimeout(() => {
            body.classList.add('preloader-finished');
        }, 3000); 
        
        setTimeout(() => {
            preloader.classList.add('hidden');
            initHeroTextAnimation();
        }, 3600);
    } else {
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
        const typingTitle = document.querySelector('.typing-title');
        if (typingTitle) {
            typingTitle.addEventListener('animationend', (e) => {
                if (e.animationName === 'typing') {
                    typingTitle.style.borderRightColor = 'transparent';
                    typingTitle.style.animation = 'blink-caret .75s step-end infinite';
                }
            });
            setTimeout(() => {
                typingTitle.classList.add('animated');
                // サブタイトルのループタイピングを開始
                loopingTypingEffect();
            }, 500);
        }
    }

    function loopingTypingEffect() {
        const subtitleElement = document.querySelector('.subtitle');
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
        const pauseEnd = 2000;
        const pauseStart = 500;

        subtitleElement.innerHTML = '';
        subtitleElement.classList.add('typing-loop');

        function type() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                // 削除中
                charIndex--;
                subtitleElement.innerHTML = currentText.substring(0, charIndex);
                if (charIndex === 0) {
                    isDeleting = false;
                    textIndex = (textIndex + 1) % texts.length;
                    setTimeout(type, pauseStart);
                } else {
                    setTimeout(type, deleteSpeed);
                }
            } else {
                // タイピング中
                charIndex++;
                subtitleElement.innerHTML = currentText.substring(0, charIndex);
                if (charIndex === currentText.length) {
                    isDeleting = true;
                    setTimeout(type, pauseEnd);
                } else {
                    setTimeout(type, typeSpeed);
                }
            }
        }
        type();
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
