document.addEventListener('DOMContentLoaded', function() {
    // AOS (Animate on Scroll) Library Initialization
    AOS.init({
        duration: 800,
        once: true,
    });

    // Interactive Particles.js Initialization
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 }},
        "color": { "value": "#ffffff" },
        "shape": { "type": "star" },
        "opacity": { "value": 0.5, "random": true },
        "size": { "value": 3, "random": true },
        "line_linked": { "enable": false },
        "move": { "enable": true, "speed": 0.5, "direction": "none", "random": true, "straight": false, "out_mode": "out" }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": { "enable": true, "mode": "repulse" },
          "onclick": { "enable": true, "mode": "push" },
          "resize": true
        },
        "modes": {
          "repulse": { "distance": 100, "duration": 0.4 },
          "push": { "particles_nb": 4 }
        }
      },
      "retina_detect": true
    });

    // --- Modal Logic ---
    const applyModal = document.getElementById('apply-modal');
    const termsModal = document.getElementById('terms-modal');
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const openTermsBtn = document.getElementById('open-terms-btn');
    const openTermsInFormBtn = document.getElementById('open-terms-in-form');
    const closeTermsBtn = document.getElementById('close-terms-btn');

    function openModal(modal) {
        if (modal) modal.classList.add('is-visible');
    }

    function closeModal(modal) {
        if (modal) modal.classList.remove('is-visible');
    }

    if (openModalBtn) {
        openModalBtn.addEventListener('click', () => openModal(applyModal));
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => closeModal(applyModal));
    }
    
    if (openTermsBtn) {
        openTermsBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(termsModal);
        });
    }
    if (openTermsInFormBtn) {
        openTermsInFormBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(termsModal);
        });
    }
    if (closeTermsBtn) {
        closeTermsBtn.addEventListener('click', () => closeModal(termsModal));
    }

    window.addEventListener('click', (e) => {
        if (e.target === applyModal) closeModal(applyModal);
        if (e.target === termsModal) closeModal(termsModal);
    });

    // --- Dynamic Form Logic ---
    const planSelect = document.getElementById('plan');
    const conceptText = document.getElementById('concept-text');
    const charCounter = document.getElementById('char-counter');
    const paypayField = document.getElementById('paypay-field');
    const paypayInput = document.getElementById('paypay-link');

    function updateFormByPlan() {
        const selectedPlan = planSelect.value;
        const minLength = 100;

        if (paypayField && paypayInput) {
            if (selectedPlan === '8G Creator Plan') {
                paypayField.style.display = 'block';
                paypayInput.required = true; // 必須項目に
            } else {
                paypayField.style.display = 'none';
                paypayInput.required = false; // 必須項目から解除
            }
        }

        if (conceptText && charCounter) {
            conceptText.required = true; // どのプランでもコンセプトは必須
            if (selectedPlan === 'Friend Plan') {
                conceptText.removeAttribute('minlength');
                charCounter.textContent = '文字数制限なし';
                charCounter.style.color = '#aaa';
            } else if (selectedPlan) { // Creatorプランが選択された場合
                conceptText.setAttribute('minlength', minLength);
                const currentLength = conceptText.value.length;
                charCounter.textContent = `${currentLength} / ${minLength} 文字以上`;
                charCounter.style.color = currentLength >= minLength ? '#25fc75' : '#aaa';
            } else { // 何も選択されていない場合
                conceptText.required = false;
                conceptText.removeAttribute('minlength');
                charCounter.textContent = '';
            }
        }
    }

    if (conceptText) {
        conceptText.addEventListener('input', () => {
            if (planSelect.value !== 'Friend Plan' && planSelect.value) {
                const minLength = 100;
                const currentLength = conceptText.value.length;
                charCounter.textContent = `${currentLength} / ${minLength} 文字以上`;
                charCounter.style.color = currentLength >= minLength ? '#25fc75' : '#aaa';
            }
        });
    }
    
    if (planSelect) {
        planSelect.addEventListener('change', updateFormByPlan);
        // モーダルが開かれた時に初期化
        openModalBtn.addEventListener('click', updateFormByPlan);
    }
    
    // --- Load Terms and Conditions ---
    const termsContent = document.getElementById('terms-content');
    if (termsContent) {
        fetch('terms.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                termsContent.innerHTML = data;
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
                termsContent.innerHTML = '<p>利用規約の読み込みに失敗しました。</p>';
            });
    }
});
