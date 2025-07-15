document.addEventListener('DOMContentLoaded', () => {

    // ===== 共通機能: ヘッダー & ナビゲーション =====
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    const hamburger = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('.main-nav');
    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            nav.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
        });
        nav.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (nav.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    nav.classList.remove('active');
                    document.body.classList.remove('no-scroll');
                }
            });
        });
    }

    // ===== 共通機能: フッターの年号 =====
    const currentYearEl = document.getElementById('current-year');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear().toString();
    }
    
    // ===== 共通機能: スクロールアニメーション =====
    const animatedElements = document.querySelectorAll('.animate-on-load, .animate-on-scroll');
    if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observerInstance) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const delay = el.dataset.animationDelay || '0s';
                    el.style.transitionDelay = delay;
                    el.classList.add('is-visible');
                    observerInstance.unobserve(el);
                }
            });
        }, { threshold: 0.1 });
        animatedElements.forEach(el => observer.observe(el));
    }
    
    // ===== status.html 専用のスクリプト =====
    if (document.querySelector('.status-dashboard')) {
        const API_BASE_URL = 'https://api.mcsrvstat.us/3/';
        const SERVERS = [
            { id: 'sutera', address: 'stellamc.jp:6908' },
            { id: 'vanilla', address: 'stellamc.jp:6910' },
            { id: 'proxy', address: 'stellamc.jp:6911' }
        ];

        const ui = {
            overall: document.getElementById('overall-status-panel'),
            sutera: document.getElementById('sutera-server-panel'),
            vanilla: document.getElementById('vanilla-server-panel'),
            other: document.getElementById('other-server-panel'),
            countdown: document.getElementById('countdown-timer'),
        };
        
        const fetchServerStatus = async (server) => {
            try {
                const response = await fetch(`${API_BASE_URL}${server.address}`);
                if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) {
                    throw new Error('Invalid API response');
                }
                const data = await response.json();
                return { ...data, id: server.id, hasError: false };
            } catch (error) {
                return { id: server.id, online: false, players: { online: 0, max: 0 }, hasError: true };
            }
        };

        const updatePanelUI = (panel, data, labelText = 'プレイヤー数') => {
            if (!panel) return;
            const wrapper = panel.parentElement;
            const indicator = panel.querySelector('.status-indicator');
            const label = panel.querySelector('.label');
            const gauge = panel.querySelector('.gauge-bar-fill');
            const errorMsg = panel.querySelector('.error-message');
            
            if (errorMsg) errorMsg.style.display = 'none';

            if (data && data.online) {
                wrapper.style.setProperty('--status-color', 'var(--success-color)');
                if (indicator) {
                    indicator.className = 'status-indicator online';
                    indicator.textContent = 'オンライン';
                }
                
                const { online, max } = data.players;
                label.textContent = `${labelText}: ${online} / ${max}`;
                if (gauge) {
                    gauge.innerHTML = '';
                    gauge.style.width = max > 0 ? `${(online / max) * 100}%` : '0%';
                }
            } else {
                wrapper.style.setProperty('--status-color', 'var(--danger-color)');
                 if (indicator) {
                    indicator.className = 'status-indicator offline';
                    indicator.textContent = 'オフライン';
                 }

                label.textContent = 'オフライン';
                if (gauge) {
                    gauge.innerHTML = '';
                    gauge.style.width = '0%';
                }
                if (data && data.hasError) {
                    label.textContent = '取得失敗';
                    if(errorMsg) {
                        errorMsg.style.display = 'block';
                        errorMsg.textContent = 'サーバー情報の取得に失敗しました。';
                    }
                }
            }
        };

        const loadAllStatuses = async () => {
            const results = await Promise.all(SERVERS.map(fetchServerStatus));
            const serverData = results.reduce((acc, r) => ({...acc, [r.id]: r }), {});

            updatePanelUI(ui.overall, serverData.proxy, '総オンラインプレイヤー数');
            updatePanelUI(ui.sutera, serverData.sutera, 'プレイヤー数');
            updatePanelUI(ui.vanilla, serverData.vanilla, 'プレイヤー数');

            const total = serverData.proxy?.online ? serverData.proxy.players.online : 0;
            const sutera = serverData.sutera?.online ? serverData.sutera.players.online : 0;
            const vanilla = serverData.vanilla?.online ? serverData.vanilla.players.online : 0;
            const otherCount = Math.max(0, total - sutera - vanilla);

            const otherData = {
                online: true, 
                players: { online: otherCount, max: total > 0 ? total : 1 },
                hasError: false
            };
            updatePanelUI(ui.other, otherData, 'プレイヤー数');
        };
        
        // 隠し要素
        const secretSequence = ['sutera-server-panel', 'vanilla-server-panel', 'other-server-panel'];
        let userSequence = [];
        document.querySelectorAll('.individual-server-panel').forEach(panel => {
            panel.addEventListener('click', () => {
                userSequence.push(panel.id);
                if (userSequence.length > secretSequence.length) userSequence.shift();
                if (userSequence.join(',') === secretSequence.join(',')) {
                    window.location.href = 'https://www.stellamc.jp/server.html';
                }
            });
        });

        // カウントダウンタイマー
        let countdown = 60;
        const countdownTimer = () => {
            countdown--;
            if (ui.countdown) ui.countdown.textContent = countdown;
            if (countdown <= 0) {
                countdown = 60;
                if (ui.countdown) ui.countdown.textContent = countdown;
            }
        };

        // 初回ロードと定期更新
        loadAllStatuses();
        setInterval(loadAllStatuses, 60000); // 60秒ごとにデータを更新
        setInterval(countdownTimer, 1000); // 1秒ごとにタイマーを更新
    }
});
