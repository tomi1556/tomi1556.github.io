const swiper = new Swiper('.swiper-container', {
  loop: true, // 無限ループを有効にする
  autoplay: {
    delay: 5000, // スライドを自動的に切り替える時間（ミリ秒）
    disableOnInteraction: true, // ユーザー操作後も自動再生を続ける
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true, // ドットナビゲーションをクリック可能にする
  },
  navigation: {
    nextEl: '.swiper-button-next', // 次のスライドボタン
    prevEl: '.swiper-button-prev', // 前のスライドボタン
  },
  speed: 800, // スライドの移動速度を800ミリ秒に設定
});

const swiper = new Swiper('.swiper-container', {
  loop: true,
  pagination: {
    el: '.swiper-pagination',
    clickable: true, // クリックで移動を有効にする
  },
});


async function fetchOnlineUsers() {
    try {
        const response = await fetch('https://mcapi.us/server/status?ip=stella.xgames.jp');
        const data = await response.json();
        document.getElementById('online-users').textContent = data.players.now;

        const onlinePlayers = document.getElementById('online-players');
        onlinePlayers.innerHTML = '';

        if (data.players && data.players.now > 0 && data.players.sample) {
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
            onlinePlayers.textContent = '現在オンラインのプレイヤーはいません。';
        }
    } catch (error) {
        console.error('エラー:', error);
        document.getElementById('online-players').textContent = 'オンラインのユーザー数を取得できませんでした';
    }
}

fetchOnlineUsers();
setInterval(fetchOnlineUsers, 60000);


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
