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
        
        const animateCountUp = (el, end) => {
            if (!el) return;
            const duration = 1200;
            const startValue = parseInt(el.dataset.currentValue || '0');
            el.dataset.currentValue = end;
            if (startValue === end) {
                el.textContent = end;
                return;
            }
            
            let startTime = null;
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
                return { ...data, id: server.id }; // IDをデータに含める
            } catch (error) {
                console.error(`Failed to fetch status for ${server.id}:`, error);
                return { id: server.id, online: false, players: { online: 0, max: 0 }, error: true };
            }
        };

        const updatePanelUI = (id, data) => {
            const panel = document.getElementById(`${id}-server-panel`);
            if (!panel) return;

            const accentBorder = panel.querySelector('.panel-accent-border');
            const playerLabel = panel.querySelector('.label');
            const gaugeBar = panel.querySelector('.gauge-bar-fill');
            const errorMsg = panel.querySelector('.error-message');
            
            if (errorMsg) errorMsg.style.display = 'none';

            if (data && data.online) {
                accentBorder.style.setProperty('--status-color', 'var(--success-color)');
                const { online, max } = data.players;
                playerLabel.textContent = `プレイヤー数: ${online} / ${max}`;
                if(gaugeBar) {
                    gaugeBar.innerHTML = ''; // スケルトン削除
                    gaugeBar.style.width = max > 0 ? `${(online / max) * 100}%` : '0%';
                }
            } else {
                accentBorder.style.setProperty('--status-color', 'var(--danger-color)');
                playerLabel.textContent = 'オフラインまたは取得失敗';
                 if(gaugeBar) {
                    gaugeBar.innerHTML = '<div class="skeleton"></div>';
                    gaugeBar.style.width = '100%';
                }
                if (data && data.error && errorMsg) {
                    errorMsg.style.display = 'block';
                    errorMsg.textContent = 'サーバー情報の取得に失敗しました。';
                }
            }
        };

        const updateOtherPanelUI = (count) => {
            const panel = document.getElementById('other-server-panel');
            if (!panel) return;
            const accentBorder = panel.querySelector('.panel-accent-border');
            const countEl = document.getElementById('other-player-count');
            
            accentBorder.style.setProperty('--status-color', 'var(--text-muted)');
            countEl.innerHTML = ''; // スケルトン削除
            animateCountUp(countEl, count);
        };

        const updateOverallPanelUI = (data) => {
            const panel = document.getElementById('overall-status-panel');
            const accentBorder = panel.querySelector('.panel-accent-border');
            const totalCountEl = document.getElementById('total-player-count');
            const errorMsg = document.getElementById('overall-error-message');
            
            errorMsg.style.display = 'none';

            if(data && data.online) {
                accentBorder.style.setProperty('--status-color', 'var(--success-color)');
                totalCountEl.innerHTML = '';
                animateCountUp(totalCountEl, data.players.online);
            } else {
                 accentBorder.style.setProperty('--status-color', 'var(--danger-color)');
                 totalCountEl.textContent = '-';
                 if(data && data.error) {
                    errorMsg.style.display = 'block';
                    errorMsg.textContent = '総合プレイヤー数の取得に失敗しました。';
                 }
            }
        };

        const loadAllStatuses = async () => {
            const results = await Promise.all(SERVERS.map(server => fetchServerStatus(server)));

            const getData = id => results.find(r => r.id === id);
            
            const proxyData = getData('proxy');
            const suteraData = getData('sutera');
            const vanillaData = getData('vanilla');
            
            // 各パネルを更新
            updateServerPanel('sutera', suteraData);
            updateServerPanel('vanilla', vanillaData);
            updateOverallPanelUI(proxyData);

            // 「その他」の計算と更新
            const totalPlayers = proxyData && proxyData.online ? proxyData.players.online : 0;
            const suteraPlayers = suteraData && suteraData.online ? suteraData.players.online : 0;
            const vanillaPlayers = vanillaData && vanillaData.online ? vanillaData.players.online : 0;
            const otherPlayers = Math.max(0, totalPlayers - suteraPlayers - vanillaPlayers);
            updateOtherPanelUI(otherPlayers);
        };

        loadAllStatuses();
        setInterval(loadAllStatuses, 60000); // 60秒ごとに更新
    }
});
