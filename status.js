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
            { id: 'sutera', address: 'stellamc.jp' }, 
            { id: 'vanilla', address: 'stellamc.jp:6910' }
        ];
        
        const animateCountUp = (el, end, duration = 800) => {
            if (el.textContent === String(end)) return; // 同じ値ならアニメーションしない
            let start = 0;
            let stepTime = Math.abs(Math.floor(duration / end));
            if (end === 0) {
                el.textContent = 0;
                return;
            }
            if (stepTime < 10) stepTime = 10;
            
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
                return { online: false, error: true };
            }
        };

        const updateServerPanel = (id, data) => {
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
                gaugeBar.innerHTML = '';
                gaugeBar.style.width = `${percentage}%`;
                const singleCountEl = document.getElementById(`${id}-player-count-single`);
                if (singleCountEl) {
                    singleCountEl.innerHTML = `<span id="${id}-count-anim">${online}</span>`;
                    animateCountUp(document.getElementById(`${id}-count-anim`), online);
                }
            } else {
                statusIndicator.className = 'status-indicator offline';
                statusText.textContent = data.error ? '取得失敗' : 'オフライン';
                playerLabel.textContent = 'プレイヤー数: - / -';
                gaugeBar.innerHTML = '';
                gaugeBar.style.width = '0%';
                if(data.error) {
                    errorMessage.textContent = 'サーバー情報の取得に失敗しました。';
                    errorMessage.style.display = 'block';
                }
                const singleCountEl = document.getElementById(`${id}-player-count-single`);
                if (singleCountEl) singleCountEl.textContent = '0';
            }
        };
        
        const updateOverallStatus = (results) => {
            const overallIndicator = document.getElementById('overall-status-indicator');
            const overallStatusText = document.getElementById('overall-status-text');
            const totalPlayerCountEl = document.getElementById('total-player-count');
            const overallErrorMsg = document.getElementById('overall-error-message');

            const onlineServers = results.filter(r => r.online);
            const totalPlayers = onlineServers.reduce((acc, curr) => acc + (curr.players ? curr.players.online : 0), 0);
            
            overallIndicator.className = onlineServers.length > 0 ? 'status-indicator online' : 'status-indicator offline';
            overallStatusText.textContent = onlineServers.length > 0 ? 'オンライン' : 'オフライン';
            
            totalPlayerCountEl.innerHTML = `<span id="total-count-anim">${totalPlayers}</span>`;
            animateCountUp(document.getElementById('total-count-anim'), totalPlayers);

            const errors = results.filter(r => r.error);
            if (errors.length > 0 && onlineServers.length === 0) {
                overallErrorMsg.textContent = '全サーバーの情報取得に失敗しました。';
                overallErrorMsg.style.display = 'block';
            } else {
                overallErrorMsg.style.display = 'none';
            }
        };

        const loadAllStatuses = async () => {
            const promises = SERVERS.map(server => fetchServerStatus(server));
            const results = await Promise.all(promises);
            updateOverallStatus(results);
        };

        // マウス追従エフェクト
        document.querySelectorAll('.status-panel').forEach(panel => {
            panel.addEventListener('mousemove', (e) => {
                const rect = panel.getBoundingClientRect();
                panel.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
                panel.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            });
        });
        
        // ★★★ 隠し要素のロジック ★★★
        const secretSequence = ['overall-status-panel', 'sutera-server-panel', 'vanilla-server-panel'];
        let userSequence = [];
        
        document.querySelectorAll('.status-panel').forEach(panel => {
            panel.addEventListener('click', () => {
                userSequence.push(panel.id);
                // 配列が長くなりすぎないように調整
                if (userSequence.length > secretSequence.length) {
                    userSequence.shift();
                }
                // シーケンスが一致するかチェック
                if (userSequence.join(',') === secretSequence.join(',')) {
                    console.log('Secret sequence triggered!');
                    window.location.href = 'https://www.stellamc.jp/server.html';
                }
            });
        });

        loadAllStatuses();
        setInterval(loadAllStatuses, 60000);
    }
});
