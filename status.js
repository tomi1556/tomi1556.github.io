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
            const isActive = hamburger.classList.toggle('active');
            nav.classList.toggle('active', isActive);
            document.body.classList.toggle('no-scroll', isActive);
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
        
        const animateCountUp = (el, end, duration = 800) => {
            if (!el || el.textContent === String(end)) return;
            let start = 0;
            const range = end - start;
            if (range === 0) { el.textContent = end; return; }
            const stepTime = Math.max(10, duration / range);
            
            const timer = setInterval(() => {
                start++;
                el.textContent = start;
                if (start >= end) {
                    el.textContent = end;
                    clearInterval(timer);
                }
            }, stepTime);
        };

        const fetchServerStatus = async (server) => {
            try {
                const response = await fetch(`${API_BASE_URL}${server.address}`);
                if (!response.ok) throw new Error(`Network response error`);
                const data = await response.json();
                updateServerPanel(server.id, data);
                return data;
            } catch (error) {
                console.error(`Failed to fetch status for ${server.id}:`, error);
                updateServerPanel(server.id, { online: false, error: true });
                return { id: server.id, online: false, error: true };
            }
        };

        const updateServerPanel = (id, data) => {
            const panel = document.getElementById(`${id}-server-panel`);
            if (!panel) return;
            const statusIndicator = document.getElementById(`${id}-status-indicator`);
            const statusText = document.getElementById(`${id}-status-text`);
            const playerLabel = document.getElementById(`${id}-player-label`);
            const gaugeBar = document.getElementById(`${id}-gauge-bar`);
            const errorMessage = document.getElementById(`${id}-error-message`);
            
            if (!statusIndicator) return;
            errorMessage.style.display = 'none';
            
            if (data.online) {
                statusIndicator.className = 'status-indicator online';
                statusText.textContent = 'オンライン';
                const online = data.players.online;
                const max = data.players.max;
                playerLabel.textContent = `プレイヤー数: ${online} / ${max}`;
                const percentage = max > 0 ? (online / max) * 100 : 0;
                if(gaugeBar) {
                    gaugeBar.innerHTML = '';
                    gaugeBar.style.width = `${percentage}%`;
                }
            } else {
                statusIndicator.className = 'status-indicator offline';
                statusText.textContent = data.error ? '取得失敗' : 'オフライン';
                playerLabel.textContent = 'プレイヤー数: - / -';
                 if(gaugeBar) {
                    gaugeBar.innerHTML = '';
                    gaugeBar.style.width = '0%';
                }
                if(data.error) {
                    errorMessage.textContent = 'サーバー情報の取得に失敗しました。';
                    errorMessage.style.display = 'block';
                }
            }
        };
        
        const updateOverallStatus = (results) => {
            const overallIndicator = document.getElementById('overall-status-indicator');
            const overallStatusText = document.getElementById('overall-status-text');
            const totalPlayerCountEl = document.getElementById('total-player-count');
            const overallErrorMsg = document.getElementById('overall-error-message');

            const getData = (id) => results.find(r => r && r.id === id) || { online: false, players: { online: 0 }};
            
            const proxyData = getData('proxy');
            const suteraData = getData('sutera');
            const vanillaData = getData('vanilla');

            const proxyOnline = proxyData.online ? (proxyData.players.online || 0) : 0;
            const suteraOnline = suteraData.online ? (suteraData.players.online || 0) : 0;
            const vanillaOnline = vanillaData.online ? (vanillaData.players.online || 0) : 0;
            const otherOnline = Math.max(0, proxyOnline - suteraOnline - vanillaOnline);

            overallIndicator.className = proxyData.online ? 'status-indicator online' : 'status-indicator offline';
            overallStatusText.textContent = proxyData.online ? 'オンライン' : 'オフライン';

            const updateCount = (id, count) => {
                const el = document.getElementById(id);
                if(el) {
                    el.innerHTML = `<span id="${id}-anim">${count}</span>`;
                    animateCountUp(document.getElementById(`${id}-anim`), count);
                }
            };

            updateCount('total-player-count', proxyOnline);
            updateCount('proxy-player-count-single', proxyOnline);
            updateCount('sutera-player-count-single', suteraOnline);
            updateCount('vanilla-player-count-single', vanillaOnline);
            updateCount('other-player-count-single', otherOnline);
            
            if (results.some(r => r.error)) {
                overallErrorMsg.textContent = '一部サーバー情報の取得に失敗しました。';
                overallErrorMsg.style.display = 'block';
            } else {
                overallErrorMsg.style.display = 'none';
            }
        };

        const loadAllStatuses = async () => {
            const promises = SERVERS.map(server => fetchServerStatus(server).then(data => ({ ...data, id: server.id })));
            const results = await Promise.all(promises);
            updateOverallStatus(results);
        };

        document.querySelectorAll('.status-panel').forEach(panel => {
            panel.addEventListener('mousemove', (e) => {
                const rect = panel.getBoundingClientRect();
                panel.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
                panel.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            });
        });
        
        const secretSequence = ['overall-status-panel', 'sutera-server-panel', 'vanilla-server-panel'];
        let userSequence = [];
        
        document.querySelectorAll('.status-panel').forEach(panel => {
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

        loadAllStatuses();
        setInterval(loadAllStatuses, 60000);
    }
});
