document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menu-button');
    const mobileNav = document.getElementById('mobile-nav');

    menuButton.addEventListener('click', () => {
        mobileNav.classList.toggle('open'); // 'open'クラスをトグル
        console.log('メニュー状態:', mobileNav.classList.contains('open') ? '開いた' : '閉じた');
    });
});

async function fetchMinecraftStatus() {
    try {
        const response = await fetch('https://mcapi.us/server/status?ip=stellamc.jp');
        const data = await response.json();

        console.log('APIレスポンス:', data); // APIレスポンスを確認

        // オンライン人数を表示
        const onlineUsers = document.getElementById('online-users');
        const onlinePlayersCount = data.players?.now || 0;
        onlineUsers.textContent = onlinePlayersCount;

        // オンラインプレイヤーリストを表示
        const onlinePlayers = document.getElementById('online-players');
        onlinePlayers.innerHTML = '';

        // プレイヤーリストが存在するか確認
        if (data.players && Array.isArray(data.players.sample)) {
            console.log('オンラインプレイヤーリスト:', data.players.sample); // プレイヤーリストの確認
            
            const bedrockPlayers = [];
            const javaPlayers = [];

            // プレイヤーを分類
            data.players.sample.forEach(player => {
                if (player.name.startsWith('.')) {
                    bedrockPlayers.push(player);
                } else {
                    javaPlayers.push(player);
                }
            });

            // 統合版プレイヤーを表示
            bedrockPlayers.forEach(player => {
                const playerDiv = createPlayerElement(player, '統合版', 'bedrock-player');
                onlinePlayers.appendChild(playerDiv);
            });

            // Java版プレイヤーを表示
            javaPlayers.forEach(player => {
                const playerDiv = createPlayerElement(player, 'Java', 'java-player');
                onlinePlayers.appendChild(playerDiv);
            });
        } else {
            console.log('プレイヤーリストが存在しないか、空です');
            onlinePlayers.textContent = 'オンラインプレイヤーの詳細情報がありません';
        }
    } catch (error) {
        console.error('Minecraftステータスの取得に失敗:', error);
        document.getElementById('online-users').textContent = 'N/A';
        document.getElementById('online-players').textContent = 'データを取得できませんでした。';
    }
}

function createPlayerElement(player, badgeText, className) {
    const playerDiv = document.createElement('div');
    playerDiv.className = `player ${className}`;

    const playerImg = document.createElement('img');
    const avatarUrl = `https://mc-heads.net/avatar/${player.name}/100`;
    playerImg.src = avatarUrl;
    playerImg.alt = `${player.name}のアバター`;

    // 画像が存在しない場合、フォールバック
    playerImg.onerror = () => {
        playerImg.src = 'https://mc-heads.net/avatar/Default/100';
    };

    const playerId = document.createElement('p');
    playerId.textContent = player.name || '不明なプレイヤー';

    const badge = document.createElement('div');
    badge.className = 'badge';
    badge.textContent = badgeText;

    playerDiv.appendChild(playerImg);
    playerDiv.appendChild(playerId);
    playerDiv.appendChild(badge);

    return playerDiv;
}

// 初回取得と定期更新
fetchMinecraftStatus();
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
