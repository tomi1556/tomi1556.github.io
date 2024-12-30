document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menu-button');
    const mobileNav = document.getElementById('mobile-nav');

    menuButton.addEventListener('click', () => {
        mobileNav.classList.toggle('open'); // 'open'クラスをトグル
        console.log('メニュー状態:', mobileNav.classList.contains('open') ? '開いた' : '閉じた');
    });
});

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


// ページロード後にローダーを非表示
window.addEventListener('load', () => {
    document.querySelector('.loader').style.display = 'none';
});

// セクションの表示/非表示
function toggleSection(id) {
    const section = document.getElementById(id);
    const sectionContent = document.getElementById('section-content');
    const title = document.getElementById('section-title');
    const description = document.getElementById('section-description');

    let sectionData = {
        'beginner': {
            title: '初心者向けの説明',
            description: 'サーバーへの参加が初めてでも大丈夫！サーバーの入り方、基本的なマナーや最初にやるべきことを詳しく解説します。'
        },
        'rules': {
            title: 'サーバー規約',
            description: '安全で楽しいサーバー運営のために、ルールをしっかり確認しましょう。禁止事項やペナルティも詳しく説明します。'
        },
        'donation': {
            title: '寄付について',
            description: 'サーバー運営は皆さんのサポートによって成り立っています。寄付の特典や方法についてご案内します。'
        },
        'basic': {
            title: '基本操作',
            description: 'マインクラフト初心者でも安心！基本操作や便利なコマンド、初歩的な建築方法を解説します。'
        }
    };

    sectionContent.style.display = 'block';
    sectionContent.classList.remove('slideIn');
    setTimeout(() => {
        sectionContent.classList.add('slideIn');
    }, 10);

    title.textContent = sectionData[id].title;
    description.textContent = sectionData[id].description;
}
