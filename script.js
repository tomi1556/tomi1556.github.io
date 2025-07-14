document.addEventListener('DOMContentLoaded', () => {

    const body = document.body;
    const preloader = document.querySelector('.preloader');
    const preloaderContainer = document.querySelector('.preloader-container');
    const pageWrapper = document.querySelector('.page-wrapper');

    // ===== Preloader (オープニングアニメーション) =====
    // 固まる問題を解決し、意図したアニメーションが実行されるように修正
    if (preloader && preloaderContainer && pageWrapper) {
        // 初期状態としてスクロールを禁止
        body.classList.add('no-scroll');

        window.addEventListener('load', () => {
            // 1. ロゴが表示された後、1秒待ってからアニメーションを開始
            setTimeout(() => {
                preloaderContainer.classList.add('animated');
            }, 1000);

            // 2. アニメーションが完了する頃 (2.8秒後) にプリローダーを消し始める
            setTimeout(() => {
                body.classList.add('preloader-finished');
                body.classList.remove('no-scroll');
                
                // 3. メインコンテンツを表示
                pageWrapper.classList.add('visible');

                // 4. プリローダーが消えるアニメーション(0.6s)が終わった頃にヒーローのタイピングを開始
                setTimeout(initHeroTextAnimation, 600);
                
            }, 2800); // 1000ms(待機) + 1800ms(アニメーション時間) = 2800ms
        });

    } else {
        // プリローダーがない場合のフォールバック
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
        
        if (titleElement) titleElement.innerHTML = '';
        if (subtitleElement) subtitleElement.innerHTML = '';
        
        if (titleElement) {
            typewriter(titleElement, "StellaMC", 120, () => {
                // タイトル表示完了後にサブタイトルのループを開始
                 if (subtitleElement) {
                    loopingTypingEffect();
                }
            });
        }
    }

    // 汎用タイピング関数
    function typewriter(element, text, speed, callback) {
        let charIndex = 0;
        element.classList.add('typing-cursor');
        element.classList.remove('blinking-cursor');

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
                // 削除処理
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
                // 入力処理
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
