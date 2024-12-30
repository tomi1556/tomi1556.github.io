// JavaScriptでメニューの開閉を制御
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('.mobile-nav');

menuButton.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
});


// ✅ Minecraftオンラインプレイヤー取得 (api.mcsrvstat.us版)
async function fetchMinecraftStatus() {
    try {
        const response = await fetch('https://api.mcsrvstat.us/2/stellamc.jp');
        const data = await response.json();

        console.log(data); // APIレスポンスをコンソールに出力して確認

        // オンライン人数を表示
        const onlineUsers = document.getElementById('online-users');
        const onlinePlayersCount = data.players?.online || 0; // 人数を取得
        onlineUsers.textContent = onlinePlayersCount; // 人数を表示

        // オンラインプレイヤーリストを表示
        const onlinePlayers = document.getElementById('online-players');
        onlinePlayers.innerHTML = ''; // リストをリセット

        if (data.players && onlinePlayersCount > 0 && data.players.list) {
            data.players.list.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player';

                const playerImg = document.createElement('img');
                playerImg.src = `https://mc-heads.net/avatar/${player}/100`;
                playerImg.alt = `${player}のアバター`;

                const playerId = document.createElement('p');
                playerId.textContent = player || '不明なプレイヤー';

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
        document.getElementById('online-players').textContent = 'データを取得できませんでした。';
    }
}

// 初回取得と定期更新
fetchMinecraftStatus();
setInterval(fetchMinecraftStatus, 60000); // 1分ごとに更新


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
