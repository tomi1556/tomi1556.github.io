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
            data.players.sample.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player';

                const playerImg = document.createElement('img');
                let avatarUrl = '';

                // プレイヤーのスキンを取得するためのAPI
                const skinUrl = await getPlayerSkinUrl(player.name);

                if (skinUrl) {
                    avatarUrl = skinUrl; // スキンURLを設定
                } else {
                    avatarUrl = 'https://mc-heads.net/avatar/Default/100'; // デフォルト画像にフォールバック
                }

                playerImg.src = avatarUrl;
                playerImg.alt = `${player.name}のアバター`;

                // 画像が存在しない場合、フォールバック
                playerImg.onerror = () => {
                    playerImg.src = 'https://mc-heads.net/avatar/Default/100'; // デフォルト画像にフォールバック
                };

                const playerId = document.createElement('p');
                playerId.textContent = player.name || '不明なプレイヤー';

                const badge = document.createElement('div');
                badge.className = 'badge';

                // Bedrockプレイヤー判定（名前の先頭が`.`の場合）
                if (player.name.startsWith('.')) {
                    playerDiv.classList.add('bedrock-player');
                    badge.textContent = 'Bedrock';
                } else {
                    playerDiv.classList.add('java-player');
                    badge.textContent = 'Java';
                }

                playerDiv.appendChild(playerImg);
                playerDiv.appendChild(playerId);
                playerDiv.appendChild(badge);
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

// プレイヤー名からスキンURLを取得する関数
async function getPlayerSkinUrl(playerName) {
    try {
        // プレイヤー名からUUIDを取得
        const uuidResponse = await fetch(`https://api.mojang.com/users/profiles/minecraft/${playerName}`);
        const uuidData = await uuidResponse.json();
        
        if (uuidData && uuidData.id) {
            // UUIDが取得できた場合、スキンURLを取得
            const skinResponse = await fetch(`https://sessionserver.mojang.com/session/minecraft/profile/${uuidData.id}`);
            const skinData = await skinResponse.json();

            if (skinData && skinData.properties) {
                // スキンデータを抽出
                const textureData = skinData.properties.find(prop => prop.name === 'textures');
                if (textureData && textureData.value) {
                    const decodedTexture = JSON.parse(atob(textureData.value)); // base64デコード
                    return decodedTexture.textures.SKIN.url; // スキン画像のURL
                }
            }
        }
        return null;
    } catch (error) {
        console.error('スキンURLの取得に失敗:', error);
        return null;
    }
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
