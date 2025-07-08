document.addEventListener('DOMContentLoaded', function() {
    // AOS (Animate on Scroll) Library Initialization
    AOS.init({
        duration: 800,
        once: true,
    });

    // Particles.js Initialization
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 80,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "star",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
        },
        "opacity": {
          "value": 0.5,
          "random": true,
        },
        "size": {
          "value": 3,
          "random": true,
        },
        "line_linked": {
          "enable": false,
        },
        "move": {
          "enable": true,
          "speed": 0.5,
          "direction": "none",
          "random": true,
          "straight": false,
          "out_mode": "out",
          "bounce": false,
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": false,
          },
          "onclick": {
            "enable": false,
          },
          "resize": true
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

    // Close modal if background is clicked
    window.addEventListener('click', (e) => {
        if (e.target === applyModal) closeModal(applyModal);
        if (e.target === termsModal) closeModal(termsModal);
    });

    // --- Form Logic ---
    const conceptText = document.getElementById('concept-text');
    const charCounter = document.getElementById('char-counter');
    const minLength = 200;

    if (conceptText && charCounter) {
        conceptText.addEventListener('input', () => {
            const currentLength = conceptText.value.length;
            charCounter.textContent = `${currentLength} / ${minLength}`;
            if (currentLength >= minLength) {
                charCounter.style.color = '#25fc75'; // Green
            } else {
                charCounter.style.color = '#aaa';
            }
        });
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
