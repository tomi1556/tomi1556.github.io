// JavaScriptでメニューの開閉を制御
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('.mobile-nav');

menuButton.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
});


// ====== ✅ Minecraftステータス取得 ======
async function fetchMinecraftStatus() {
    try {
        const response = await fetch('https://mcapi.us/server/status?ip=stellamc.jp');
        const data = await response.json();

        console.log(data); // APIレスポンスをコンソールに出力して確認

        // オンライン人数を取得
        const onlinePlayersCount = data.players?.online || data.players?.now || 'N/A';
        
        // 両方の要素に人数を表示
        document.getElementById('online-users').textContent = onlinePlayersCount;

        // オンラインプレイヤーリストを表示
        const onlinePlayers = document.getElementById('online-players');
        onlinePlayers.innerHTML = '';

        if (data.players && onlinePlayersCount > 0 && data.players.sample) {
            data.players.sample.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player';

                const playerImg = document.createElement('img');
                playerImg.src = `https://mc-heads.net/avatar/${player.id}/100`;

                const playerId = document.createElement('p');
                playerId.textContent = player.name;

                playerDiv.appendChild(playerImg);
                playerDiv.appendChild(playerId);
                onlinePlayers.appendChild(playerDiv);
            });
        } else {
            onlinePlayers.textContent = 'オンラインプレイヤーはいません';
        }
    } catch (error) {
        console.error('Minecraftステータスの取得に失敗:', error);
        document.getElementById('online-users').textContent = 'N/A';
    }
}

// 初期読み込み時に呼び出し
fetchMinecraftStatus();

// 1分ごとにMinecraftステータスを更新
setInterval(fetchMinecraftStatus, 60000); // 60000ミリ秒 = 1分


// ====== ✅ ページ読み込み時と定期実行 ======
document.addEventListener('DOMContentLoaded', () => {
    fetchMinecraftStatus();
    fetchDiscordStatus();
});
setInterval(fetchMinecraftStatus, 60000); // 1分ごとに更新

// ====== ✅ メニューボタンのクリックイベント ======
const menuButton = document.querySelector('.menu-button');
const body = document.querySelector('body');

menuButton.addEventListener('click', function() {
    body.classList.toggle('menu-open');
    document.querySelector('nav').classList.toggle('menu-open');
});

// ====== ✅ フェードイン要素の監視 ======
const fadeInElements = document.querySelectorAll(".fade-in");

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target); // 一度だけアニメーションを適用
        }
    });
});

fadeInElements.forEach(el => observer.observe(el));


// ====== ✅ コピー機能 ======
function copyToClipboard(address, button) {
    navigator.clipboard.writeText(address).then(() => {
        button.textContent = '完了！';
        button.classList.add('copy-success');
        setTimeout(() => {
            button.textContent = 'コピー';
            button.classList.remove('copy-success');
        }, 2000);
    }).catch(err => {
        console.error('エラー:', err);
        button.textContent = 'エラー';
        button.classList.add('copy-fail');
        setTimeout(() => {
            button.textContent = 'コピー';
            button.classList.remove('copy-fail');
        }, 2000);
    });
}
