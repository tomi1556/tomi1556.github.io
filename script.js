document.addEventListener('DOMContentLoaded', () => {

    // ===== Preloader (オープニングアニメーション) =====
    const body = document.body;
    const preloader = document.querySelector('.preloader');
    const preloaderContainer = document.querySelector('.preloader-container');

    if (preloader) {
        // アニメーションのシーケンスを開始
        setTimeout(() => {
            if(preloaderContainer) preloaderContainer.classList.add('animated');
        }, 1200);

        // 全体のアニメーションが完了し、サイトを表示するタイミング
        setTimeout(() => {
            body.classList.add('preloader-finished');
        }, 3000); 
        
        // プリローダー要素自体をDOMから隠すタイミング
        setTimeout(() => {
            preloader.classList.add('hidden');
            initHeroTextAnimation();
        }, 3600);
    } else {
        // プリローダーがない場合は直接ヒーローアニメーションを開始
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
        
        if (titleElement) {
            typewriter(titleElement, "StellaMC", 150, () => {
                loopingTypingEffect();
            });
        }
    }

    // 汎用タイピング関数
    function typewriter(element, text, speed, callback) {
        let charIndex = 0;
        element.innerHTML = '';
        element.classList.add('typing-cursor');

        function type() {
            if (charIndex < text.length) {
                element.textContent += text.charAt(charIndex);
                charIndex++;
                setTimeout(type, speed + (Math.random() * 40 - 20));
            } else {
                element.classList.remove('typing-cursor');
                element.classList.add('blinking-cursor'); //完了後に点滅開始
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
