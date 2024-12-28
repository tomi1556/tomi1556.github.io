const fadeInElements = document.querySelectorAll(".fade-in");

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target); // 一度だけアニメーションを適用する場合
    }
  });
});

fadeInElements.forEach(el => observer.observe(el));


// タブの切り替え機能
const tabButtons = document.querySelectorAll('.tab-button');
const tabPanes = document.querySelectorAll('.tab-pane');

tabButtons.forEach(button => {
  button.addEventListener('click', () => {
    // すべてのボタンから"active"クラスを削除
    tabButtons.forEach(btn => btn.classList.remove('active'));
    // クリックしたボタンに"active"クラスを追加
    button.classList.add('active');
    
    // すべてのタブコンテンツから"active"クラスを削除
    tabPanes.forEach(pane => pane.classList.remove('active'));
    // 選択したタブのコンテンツを表示
    document.getElementById(button.getAttribute('data-tab')).classList.add('active');
  });
});


const swiper = new Swiper('.swiper-container', {
  loop: true, // 無限ループを有効にする
  autoplay: {
    delay: 4000, // スライドを自動的に切り替える時間（ミリ秒）
    disableOnInteraction: false, // ユーザー操作後も自動再生を続ける
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true, // ドットナビゲーションをクリック可能にする
  },
  slidesPerView: 'auto', // 各スライドの幅を自動的に調整
  spaceBetween: 0, // スライド間の隙間を調整
  navigation: false,
  speed: 800, // スライドの移動速度を800ミリ秒に設定
});


async function fetchOnlineUsers() {
    try {
        const response = await fetch('https://mcapi.us/server/status?ip=stellamc.jp');
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
            onlinePlayers.textContent = '　';
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

document.querySelector('.menu-button').addEventListener('click', function() {
    const nav = document.querySelector('nav');
    nav.classList.toggle('menu-open');
});

