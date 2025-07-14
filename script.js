document.addEventListener('DOMContentLoaded', () => {

    const body = document.body;
    const preloader = document.querySelector('.preloader');
    const preloaderContainer = document.querySelector('.preloader-container');
    const pageWrapper = document.querySelector('.page-wrapper');

    // ===== Preloader (オープニングアニメーション) =====
    if (preloader && preloaderContainer && pageWrapper) {
        body.classList.add('no-scroll');

        window.addEventListener('load', () => {
            setTimeout(() => {
                preloaderContainer.classList.add('animated');
            }, 1000);

            setTimeout(() => {
                body.classList.add('preloader-finished');
                body.classList.remove('no-scroll');
                pageWrapper.classList.add('visible');
                setTimeout(initHeroTextAnimation, 600);
            }, 2800);
        });

    } else {
        if(pageWrapper) pageWrapper.classList.add('visible');
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
        
        if (subtitleElement) subtitleElement.innerHTML = '';
        
        if (titleElement) {
            titleElement.textContent = "StellaMC";
            if (subtitleElement) {
                loopingTypingEffect();
            }
        }
    }

    // サブタイトルのループタイピング関数
    function loopingTypingEffect() {
        const subtitleElement = document.getElementById('typing-subtitle');
        if (!subtitleElement) return;

        const texts = [
            "安心できるからこそ、本気で楽しめる。",
            "心安らぐ、あなたのもう一つの居場所。",
            "最高のコミュニティと冒険がここに。",
            "Java版 & 統合版クロスプレイ対応！"
        ];
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typeSpeed = 100;
        const deleteSpeed = 50;
        const pauseEnd = 2200;

        function loop() {
            subtitleElement.classList.add('typing-cursor');
            subtitleElement.classList.remove('blinking-cursor');
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                subtitleElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                if (charIndex === 0) {
                    isDeleting = false;
                    textIndex = (textIndex + 1) % texts.length;
                    setTimeout(loop, 500);
                } else {
                    setTimeout(loop, deleteSpeed);
                }
            } else {
                subtitleElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                if (charIndex === currentText.length) {
                    isDeleting = true;
                    subtitleElement.classList.remove('typing-cursor');
                    subtitleElement.classList.add('blinking-cursor');
                    setTimeout(loop, pauseEnd);
                } else {
                    setTimeout(loop, typeSpeed);
                }
            }
        }
        loop();
    }


    // ===== Footer Year (フッターの年号) =====
    const currentYearEl = document.getElementById('current-year');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear().toString();
    }

    // ===== Clipboard (コピー機能) =====
    // ★★★ どの環境でも動作するようにフォールバック処理を追加 ★★★
    const copyBtns = document.querySelectorAll('.copy-action-btn');
    const toast = document.getElementById('copy-toast');

    async function copyToClipboard(text, element) {
        try {
            // モダンな方法 (HTTPS必須)
            await navigator.clipboard.writeText(text);
            showToast(true, element.getAttribute('aria-label'));
        } catch (err) {
            // モダンな方法が失敗した場合、従来の非推奨な方法を試す
            legacyCopyToClipboard(text, element);
        }
    }
    
    function legacyCopyToClipboard(text, element) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        
        // 画面外に要素を配置
        textArea.style.position = "fixed";
        textArea.style.top = "-9999px";
        textArea.style.left = "-9999px";
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showToast(true, element.getAttribute('aria-label'));
            } else {
                showToast(false);
            }
        } catch (err) {
            showToast(false);
        }
        
        document.body.removeChild(textArea);
    }

    function showToast(success, message = '') {
        if (toast) {
            if (success) {
                toast.textContent = `${message.replace('をコピー', '')} をコピーしました！`;
                toast.className = 'copy-toast show';
            } else {
                toast.textContent = 'コピーに失敗しました';
                toast.className = 'copy-toast show error';
            }
            setTimeout(() => { toast.className = 'copy-toast'; }, 2000);
        }
    }

    if (copyBtns.length > 0) {
        copyBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetSelector = btn.getAttribute('data-clipboard-target');
                const inputEl = document.querySelector(targetSelector);
                if (inputEl && inputEl.value) {
                    copyToClipboard(inputEl.value, btn);
                }
            });
        });
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
