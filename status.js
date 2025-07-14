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
        
        const animateCountUp = (el, end, duration = 1200) => {
            if (!el) return;
            const startValue = parseInt(el.textContent) || 0;
            if (startValue === end) return;
            
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
                return await response.json();
            } catch (error) {
                console.error(`Failed to fetch status for ${server.id}:`, error);
                return { online: false, error: true };
            }
        };

        const updateServerPanel = (id, data) => {
            const panel = document.getElementById(`${id}-server-panel`);
            if (!panel) return;

            const indicator = document.getElementById(`${id}-status-indicator`);
            const text = document.getElementById(`${id}-status-text`);
            const label = document.getElementById(`${id}-player-label`);
            const gauge = document.getElementById(`${id}-gauge-bar`);
            const errorMsg = document.getElementById(`${id}-error-message`);
            
            if (!indicator) return;

            errorMsg.style.display = 'none';

            if (data && data.online) {
                indicator.className = 'status-indicator online';
                text.textContent = 'オンライン';
                const { online, max } = data.players;
                label.textContent = `プレイヤー数: ${online} / ${max}`;
                gauge.innerHTML = '';
                gauge.style.width = max > 0 ? `${(online / max) * 100}%` : '0%';
            } else {
                indicator.className = 'status-indicator offline';
                text.textContent = data && data.error ? '取得失敗' : 'オフライン';
                label.textContent = 'プレイヤー数: - / -';
                gauge.innerHTML = '<div class="skeleton"></div>';
                gauge.style.width = '100%';
                if (data && data.error) {
                    errorMsg.style.display = 'block';
                    errorMsg.textContent = 'サーバー情報の取得に失敗しました。';
                }
            }
        };

        const updateOtherPanel = (count) => {
            const panel = document.getElementById('other-server-panel');
            if (!panel) return;

            const indicator = document.getElementById('other-status-indicator');
            const text = document.getElementById('other-status-text');
            const countEl = document.getElementById('other-player-count');

            indicator.className = 'status-indicator online';
            text.textContent = 'ロビー等';
            countEl.innerHTML = '';
            animateCountUp(countEl, count);
        };

        const loadAllStatuses = async () => {
            const promises = SERVERS.map(server => fetchServerStatus(server).then(data => ({...data, id: server.id })));
            const results = await Promise.all(promises);

            const getData = id => results.find(r => r.id === id) || { online: false, players: { online: 0 }};
            
            const proxyData = getData('proxy');
            const suteraData = getData('sutera');
            const vanillaData = getData('vanilla');

            // 各パネルを更新
            updateServerPanel('sutera', suteraData);
            updateServerPanel('vanilla', vanillaData);
            
            // 総合パネルの更新
            const totalPlayers = proxyData.online ? proxyData.players.online : 0;
            const totalCountEl = document.getElementById('total-player-count');
            if(totalCountEl) {
                totalCountEl.innerHTML = '';
                animateCountUp(totalCountEl, totalPlayers);
            }
            const overallError = document.getElementById('overall-error-message');
            if(proxyData.error) {
                overallError.style.display = 'block';
                overallError.textContent = '総合プレイヤー数の取得に失敗しました。';
                totalCountEl.textContent = '-';
            } else {
                overallError.style.display = 'none';
            }

            // 「その他」の計算と更新
            const suteraPlayers = suteraData.online ? suteraData.players.online : 0;
            const vanillaPlayers = vanillaData.online ? vanillaData.players.online : 0;
            const otherPlayers = Math.max(0, totalPlayers - suteraPlayers - vanillaPlayers);
            updateOtherPanel(otherPlayers);
        };

        // マウス追従エフェクト
        document.querySelectorAll('.status-panel').forEach(panel => {
            panel.addEventListener('mousemove', (e) => {
                const rect = panel.getBoundingClientRect();
                panel.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
                panel.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            });
        });

        loadAllStatuses();
        setInterval(loadAllStatuses, 60000); // 60秒ごとに更新
    }
});
