// ページロード時のアニメーション
window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');
    setTimeout(() => {
        loader.style.display = 'none';
    }, 1500);
});

// スクロール時のセクション表示
const sections = document.querySelectorAll('.fade-in');

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.2 });

sections.forEach(section => {
    observer.observe(section);
});

// スクロール関数
function scrollToSection(id) {
    const section = document.getElementById(id);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}
