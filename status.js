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

        // UI要素を最初にキャッシュ
        const ui = {
            overall: {
                panel: document.getElementById('overall-status-panel'),
                accent: document.querySelector('#overall-status-panel .panel-accent-border'),
                count: document.getElementById('total-player-count'),
                error: document.getElementById('overall-error-message')
            },
            sutera: {
                panel: document.getElementById('sutera-server-panel'),
                accent: document.querySelector('#sutera-server-panel .panel-accent-border'),
                label: document.getElementById('sutera-player-label'),
                gauge: document.getElementById('sutera-gauge-bar'),
                error: document.getElementById('sutera-error-message')
            },
            vanilla: {
                panel: document.getElementById('vanilla-server-panel'),
                accent: document.querySelector('#vanilla-server-panel .panel-accent-border'),
                label: document.getElementById('vanilla-player-label'),
                gauge: document.getElementById('vanilla-gauge-bar'),
                error: document.getElementById('vanilla-error-message')
            },
            other: {
                panel: document.getElementById('other-server-panel'),
                accent: document.querySelector('#other-server-panel .panel-accent-border'),
                count: document.getElementById('other-player-count')
            }
        };
        
        const animateCountUp = (el, end) => {
            if (!el) return;
            const startValue = parseInt(el.dataset.currentValue || '0');
            el.dataset.currentValue = end;
            if (startValue === end) { el.textContent = end; return; }
            
            let startTime;
            const duration = 1200;
            const step = (timestamp) => {
                if (!startTime) startTime = timestamp;
                const progress = Math.min((timestamp - startTime) / duration, 1);
                const easeOut = 1 - Math.pow(1 - progress, 4);
                el.textContent = Math.floor(easeOut * (end - startValue) + startValue);
                if (progress < 1) window.requestAnimationFrame(step);
            };
            window.requestAnimationFrame(step);
        };

        const fetchServerStatus = async (server) => {
            try {
                const response = await fetch(`${API_BASE_URL}${server.address}`);
                if (!response.ok) throw new Error('Network response error');
                const data = await response.json();
                return { ...data, id: server.id };
            } catch (error) {
                return { id: server.id, online: false, players: { online: 0, max: 0 }, error: true };
            }
        };

        const updatePanelUI = (id, data) => {
            const elements = ui[id];
            if (!elements || !elements.panel) return;

            elements.error.style.display = 'none';

            if (data && data.online) {
                elements.accent.style.setProperty('--status-color', 'var(--success-color)');
                const { online, max } = data.players;
                elements.label.textContent = `プレイヤー数: ${online} / ${max}`;
                if(elements.gauge) {
                    elements.gauge.innerHTML = '';
                    elements.gauge.style.width = max > 0 ? `${(online / max) * 100}%` : '0%';
                }
            } else {
                elements.accent.style.setProperty('--status-color', 'var(--danger-color)');
                elements.label.textContent = 'オフライン';
                if(elements.gauge) {
                    elements.gauge.innerHTML = '';
                    elements.gauge.style.width = '0%';
                }
                if (data && data.error) {
                    elements.label.textContent = '取得失敗';
                    elements.error.style.display = 'block';
                    elements.error.textContent = 'サーバー情報の取得に失敗しました。';
                }
            }
        };

        const loadAllStatuses = async () => {
            const results = await Promise.all(SERVERS.map(fetchServerStatus));
            const serverData = {};
            results.forEach(r => { serverData[r.id] = r; });

            // 総合パネルの更新
            if (serverData.proxy && serverData.proxy.online) {
                ui.overall.accent.style.setProperty('--status-color', 'var(--success-color)');
                ui.overall.error.style.display = 'none';
                animateCountUp(ui.overall.count, serverData.proxy.players.online);
            } else {
                ui.overall.accent.style.setProperty('--status-color', 'var(--danger-color)');
                ui.overall.count.textContent = '-';
                if(serverData.proxy && serverData.proxy.error) {
                    ui.overall.error.style.display = 'block';
                    ui.overall.error.textContent = '総合プレイヤー数の取得に失敗しました。';
                }
            }

            // 各サーバーパネルの更新
            updatePanelUI('sutera', serverData.sutera);
            updatePanelUI('vanilla', serverData.vanilla);

            // 「その他」の計算と更新
            const total = serverData.proxy && serverData.proxy.online ? serverData.proxy.players.online : 0;
            const sutera = serverData.sutera && suteraData.sutera.online ? serverData.sutera.players.online : 0;
            const vanilla = serverData.vanilla && serverData.vanilla.online ? serverData.vanilla.players.online : 0;
            const other = Math.max(0, total - sutera - vanilla);

            ui.other.accent.style.setProperty('--status-color', 'var(--text-muted)');
            animateCountUp(ui.other.count, other);
        };
        
        // ★★★ 隠し要素のロジック ★★★
        const secretSequence = ['sutera-server-panel', 'vanilla-server-panel', 'other-server-panel'];
        let userSequence = [];
        document.querySelectorAll('.individual-server-panel').forEach(panel => {
            panel.addEventListener('click', () => {
                userSequence.push(panel.id);
                if (userSequence.length > secretSequence.length) {
                    userSequence.shift();
                }
                if (userSequence.join(',') === secretSequence.join(',')) {
                    window.location.href = 'https://www.stellamc.jp/server.html';
                }
            });
        });

        // 初回ロードと定期更新
        loadAllStatuses();
        setInterval(loadAllStatuses, 60000);
    }
});
