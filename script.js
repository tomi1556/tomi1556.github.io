document.addEventListener('DOMContentLoaded', () => {

    const body = document.body;
    const preloader = document.querySelector('.preloader');
    const preloaderContainer = document.querySelector('.preloader-container');
    const pageWrapper = document.querySelector('.page-wrapper');

    // ===== Preloader (オープニングアニメーション) =====
    // サイト読み込みが完了したらプリローダーのアニメーションを開始
    if (preloader && preloaderContainer && pageWrapper) {
        // body.classList.add('no-scroll'); はHTMLで初期設定済み
        
        window.addEventListener('load', () => {
            // ロゴの移動アニメーション開始
            setTimeout(() => {
                preloaderContainer.classList.add('animated');
            }, 1000); // 1秒後にロゴ移動開始

            // プリローダー非表示とサイトコンテンツ表示
            setTimeout(() => {
                body.classList.add('preloader-finished');
                body.classList.remove('no-scroll'); // スクロール禁止解除
                pageWrapper.classList.add('visible'); // メインコンテンツ表示
                
                // サイト表示後にアニメーション関連の初期化を実行
                // CSSトランジションと重ならないよう少し遅延させる
                setTimeout(initEnhancedFeatures, 600); 
            }, 2800); // プリローダーを完全に非表示にするまでの合計時間
        });

    } else {
        // プリローダーがない場合、すぐにコンテンツを表示し、機能を初期化
        if(pageWrapper) pageWrapper.classList.add('visible');
        initEnhancedFeatures();
    }

    // ===== すべての強化機能の初期化 =====
    function initEnhancedFeatures() {
        initHeroTextAnimation();
        initSpotlightEffect();
        initParallaxEffect();
        initCard3DEffect();
        initScrollAnimations(); // Intersection Observerの初期化をここで行う
    }
    
    // ===== Header & Navigation (ヘッダーとナビゲーション) =====
    const header = document.querySelector('header');
    const hamburger = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('.main-nav');
    const navLinks = document.querySelectorAll('.main-nav .nav-link');

    if (header) {
        window.addEventListener('scroll', () => {
            // スクロール量が20pxを超えたらヘッダーに'scrolled'クラスを追加
            header.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            const isActive = hamburger.classList.toggle('active');
            nav.classList.toggle('active', isActive);
            document.body.classList.toggle('no-scroll', isActive); // ハンバーガーメニュー展開中は背景スクロール禁止
            hamburger.setAttribute('aria-expanded', isActive.toString());
        });

        // ナビリンククリックでメニューを閉じる
        navLinks.forEach(link => {
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

        let mouseX = 0;
        let mouseY = 0;
        let currentX = 0;
        let currentY = 0;
        const speed = 0.1; // 追従速度

        function animateSpotlight() {
            currentX += (mouseX - currentX) * speed;
            currentY += (mouseY - currentY) * speed;
            spotlight.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;
            requestAnimationFrame(animateSpotlight);
        }

        window.addEventListener('mousemove', e => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        animateSpotlight(); // アニメーションループ開始
    }

    // ===== 強化: ヒーローセクションの視差効果 =====
    function initParallaxEffect() {
        const heroText = document.querySelector('.hero-text-content');
        if(!heroText) return;
        
        let ticking = false; // requestAnimationFrameの重複を防ぐ
        function updateParallax() {
            const offset = window.scrollY;
            // 垂直方向の移動量を調整 (例: 0.3倍速)
            heroText.style.transform = `translateY(${offset * 0.3}px)`;
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateParallax);
                ticking = true;
            }
        });
    }

    // ===== 強化: 特徴カードの3Dホバーエフェクト（スムーズ化） =====
    function initCard3DEffect() {
        const cards = document.querySelectorAll('.feature-card');
        cards.forEach(card => {
            let timeoutId; // ホバー終了時のタイムアウトを管理

            card.addEventListener('mousemove', e => {
                // ホバー中のみ高速トランジションを適用
                card.style.transition = 'transform 0.1s linear, box-shadow var(--transition-normal), border-color var(--transition-normal)';
                
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                // 傾き強度を調整
                const rotateX = (y - centerY) / 18; 
                const rotateY = (centerX - x) / 18;

                card.style.transform = `perspective(1000px) rotateX(${-rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });

            card.addEventListener('mouseleave', () => {
                // ホバー終了時、ゆっくり元の位置に戻るトランジション
                card.style.transition = 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1), box-shadow var(--transition-normal), border-color var(--transition-normal)';
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
    }

    // ===== Hero Text Animation (ヒーローテキストのアニメーション) =====
    function initHeroTextAnimation() {
        const titleElement = document.getElementById('typing-title');
        const subtitleElement = document.getElementById('typing-subtitle');
        
        if (titleElement) {
            // タイトルは固定テキストのため、直接設定
            titleElement.textContent = "StellaMC";
        }
        
        if (subtitleElement) {
            // サブタイトルはタイピングアニメーションをループ
            loopingTypingEffect();
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
        const typeSpeed = 100; // タイピング速度 (ms)
        const deleteSpeed = 50; // 削除速度 (ms)
        const pauseEnd = 2200; // 一時停止時間 (ms)

        function loop() {
            subtitleElement.classList.add('typing-cursor'); // カーソル表示
            subtitleElement.classList.remove('blinking-cursor'); // 点滅解除

            const currentText = texts[textIndex];
            
            if (isDeleting) {
                // 削除中
                subtitleElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                if (charIndex === 0) {
                    isDeleting = false;
                    textIndex = (textIndex + 1) % texts.length; // 次のテキストへ
                    setTimeout(loop, 500); // 次のタイピングまでの待機
                } else {
                    setTimeout(loop, deleteSpeed);
                }
            } else {
                // タイピング中
                subtitleElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                if (charIndex === currentText.length) {
                    isDeleting = true;
                    subtitleElement.classList.remove('typing-cursor'); // タイピングカーソル非表示
                    subtitleElement.classList.add('blinking-cursor'); // 点滅カーソル表示
                    setTimeout(loop, pauseEnd); // テキスト表示後の待機
                } else {
                    setTimeout(loop, typeSpeed);
                }
            }
        }
        loop(); // アニメーション開始
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
            // navigator.clipboard が使えないブラウザ（古いIEなど）へのフォールバック
            legacyCopyToClipboard(text, element);
        }
    }
    
    // 古いブラウザ用のコピー機能
    function legacyCopyToClipboard(text, element) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        // 画面外に配置
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

    function showToast(success, ariaLabel) {
        if (toast) {
            if (success) {
                // aria-labelから「をコピー」を除去して表示
                const message = ariaLabel.replace(/をコピー$/, '');
                toast.textContent = `${message} をコピーしました！`;
                toast.className = 'copy-toast show'; // 'error'クラスを確実に除去
            } else {
                toast.textContent = 'コピーに失敗しました';
                toast.className = 'copy-toast show error'; // エラー時は'error'クラスを追加
            }
            // 2秒後にトーストを非表示にする
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
    // Intersection Observerを使って要素がビューポートに入ったらアニメーション
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll, .animate-on-load');
        if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries, observerInstance) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const el = entry.target;
                        const animationDelay = el.dataset.animationDelay || '0s';
                        el.style.transitionDelay = animationDelay;
                        el.classList.add('is-visible');
                        observerInstance.unobserve(el); // 一度アニメーションしたら監視を停止
                    }
                });
            }, { 
                threshold: 0.15, // 要素の15%が表示されたら発火
                rootMargin: "0px 0px -10% 0px" // ビューポートの下端から10%手前で発火
            });

            animatedElements.forEach(el => {
                // 'animate-on-load'はプリローダー処理後に表示されるため、observerで監視。
                // ただし、ヒーローセクションの要素はプリローダーのタイムアウトと連携するため、
                // data-animation-delayが設定されているもののみobserverで監視する方が適切。
                // この実装では、すべての.animate-on-load要素をobserverで監視し、プリローダーの
                // setTimeout(initEnhancedFeatures, 600)が遅延として機能する。
                // ヒーローセクションのものはCSSで.is-visibleを直接適用するか、
                // より精密なJS制御が必要だが、現在のCSSアニメーション定義と連携させる。
                observer.observe(el);
            });
        }
    }
});
