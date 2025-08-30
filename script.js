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
                // サイト表示後にアニメーション関連の初期化を実行
                setTimeout(initEnhancedFeatures, 600);
            }, 2800);
        });

    } else {
        // プリローダーがない場合も初期化
        if(pageWrapper) pageWrapper.classList.add('visible');
        initEnhancedFeatures();
    }

    // ===== すべての強化機能の初期化 =====
    function initEnhancedFeatures() {
        initHeroTextAnimation();
        initSpotlightEffect();
        initParallaxEffect();
        initCard3DEffect();
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
    
    // ===== 強化: マウス追従スポットライト =====
    function initSpotlightEffect() {
        const spotlight = document.getElementById('spotlight');
        if (!spotlight) return;

        window.addEventListener('mousemove', e => {
            // requestAnimationFrameを使用してパフォーマンスを最適化
            window.requestAnimationFrame(() => {
                spotlight.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
            });
        });
    }

    // ===== 強化: ヒーローセクションの視差効果 =====
    function initParallaxEffect() {
        const heroText = document.querySelector('.hero-text-content');
        if(!heroText) return;
        
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const offset = window.scrollY;
                    heroText.style.transform = `translateY(${offset * 0.3}px)`;
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    // ===== 強化: 特徴カードの3Dホバーエフェクト（スムーズ化） =====
    function initCard3DEffect() {
        const cards = document.querySelectorAll('.feature-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                // ホバー開始時にトランジションを短くして反応を良くする
                card.style.transition = 'transform 0.1s linear, box-shadow var(--transition-normal), border-color var(--transition-normal)';
            });
            
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 15; // 回転強度を少し弱めて上品に
                const rotateY = (centerX - x) / 15;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });

            card.addEventListener('mouseleave', () => {
                // ホバー終了時にゆっくり元の位置に戻るトランジション
                card.style.transition = 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1), box-shadow var(--transition-normal), border-color var(--transition-normal)';
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
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
    const copyBtns = document.querySelectorAll('.copy-action-btn');
    const toast = document.getElementById('copy-toast');

    async function copyToClipboard(text, element) {
        try {
            await navigator.clipboard.writeText(text);
            showToast(true, element.getAttribute('aria-label'));
        } catch (err) {
            legacyCopyToClipboard(text, element);
        }
    }
    
    function legacyCopyToClipboard(text, element) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
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
