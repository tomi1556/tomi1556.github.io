responsive: [
  {
    breakpoint: 768,
    settings: {
      slidesToShow: 1,
      slidesToScroll: 1
    }
  },
  {
    breakpoint: 1024,
    settings: {
      slidesToShow: 2,
      slidesToScroll: 1
    }
  }
]



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
