// ページロードアニメーション
window.addEventListener('load', () => {
    document.querySelector('.loader').style.display = 'none';
});

// セクションの表示/非表示
function toggleSection(id) {
    const section = document.getElementById(id);
    section.style.display = section.style.display === 'block' ? 'none' : 'block';
    section.scrollIntoView({ behavior: 'smooth' });
}
