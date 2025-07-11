document.addEventListener('DOMContentLoaded', function() {
    // Page Loader Logic
    window.addEventListener('load', () => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('loaded');
        }
        updateProgressBars();
    });

    // AOS (Animate on Scroll) Library Initialization
    AOS.init({ duration: 800, once: true, delay: 100 });

    // Particles.js Initialization
    particlesJS("particles-js", { "particles": { "number": { "value": 80, "density": { "enable": true, "value_area": 800 }}, "color": { "value": "#ffffff" }, "shape": { "type": "star" }, "opacity": { "value": 0.5, "random": true }, "size": { "value": 3, "random": true }, "line_linked": { "enable": false }, "move": { "enable": true, "speed": 0.5, "direction": "none", "random": true, "straight": false, "out_mode": "out" }}, "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" }, "resize": true }, "modes": { "repulse": { "distance": 100, "duration": 0.4 }, "push": { "particles_nb": 4 }}}, "retina_detect": true });

    // Modal Logic
    const applyModal = document.getElementById('apply-modal');
    const termsModal = document.getElementById('terms-modal');
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const openTermsBtn = document.getElementById('open-terms-btn');
    const openTermsInFormBtn = document.getElementById('open-terms-in-form');
    const closeTermsBtn = document.getElementById('close-terms-btn');

    function openModal(modal) { if (modal) modal.classList.add('is-visible'); }
    function closeModal(modal) { if (modal) modal.classList.remove('is-visible'); }
    if (openModalBtn) openModalBtn.addEventListener('click', () => { openModal(applyModal); });
    if (closeModalBtn) closeModalBtn.addEventListener('click', () => closeModal(applyModal));
    if (openTermsBtn) openTermsBtn.addEventListener('click', (e) => { e.preventDefault(); openModal(termsModal); });
    if (openTermsInFormBtn) openTermsInFormBtn.addEventListener('click', (e) => { e.preventDefault(); openModal(termsModal); });
    if (closeTermsBtn) closeTermsBtn.addEventListener('click', () => closeModal(termsModal));
    window.addEventListener('click', (e) => {
        if (e.target === applyModal) closeModal(applyModal);
        if (e.target === termsModal) closeModal(termsModal);
    });

    // Spotlight Button Animation
    const spotlightBtn = document.querySelector('.cta-button.primary');
    if (spotlightBtn) {
        spotlightBtn.addEventListener('mousemove', e => {
            const rect = spotlightBtn.getBoundingClientRect();
            spotlightBtn.style.setProperty('--mouse-x', e.clientX - rect.left + 'px');
            spotlightBtn.style.setProperty('--mouse-y', e.clientY - rect.top + 'px');
        });
    }

    // Progress Bar (Donut Chart) Update Function
    function updateProgressBars() {
        function setRingProgress(ring, percent) {
            if (!ring) return;
            const radius = ring.r.baseVal.value;
            const circumference = 2 * Math.PI * radius;
            ring.style.strokeDasharray = `${circumference} ${circumference}`;
            const offset = circumference - (percent * circumference);
            setTimeout(() => { ring.style.strokeDashoffset = offset; }, 300);
        }
        const friendAvailable = parseInt(document.getElementById('friend-slots-available').textContent);
        setRingProgress(document.getElementById('friend-progress-ring'), friendAvailable / 3);
        const creatorAvailable = parseInt(document.getElementById('creator-slots-available').textContent);
        setRingProgress(document.getElementById('creator-progress-ring'), creatorAvailable / 5);
    }
    
    // Multi-Step Form Logic
    const form = document.getElementById('apply-form');
    if(form) {
        const steps = [...form.querySelectorAll('.form-step')];
        const stepperItems = [...form.querySelectorAll('.step')];
        const planSelectCards = [...form.querySelectorAll('.plan-select-card')];
        const planInput = document.getElementById('plan-input');
        const mcidInput = document.getElementById('mcid');
        const discordInput = document.getElementById('discord-id');
        const conceptText = document.getElementById('concept-text');
        const charCounter = document.getElementById('char-counter');
        const termsAgree = document.getElementById('terms-agree');
        
        let currentStep = 1;

        const goToStep = (stepNumber) => {
            currentStep = stepNumber;
            steps.forEach(step => {
                step.classList.toggle('active', parseInt(step.dataset.step) === currentStep);
            });
            stepperItems.forEach((step) => {
                const indicator = step.dataset.stepIndicator;
                step.classList.toggle('active', parseInt(indicator) === currentStep);
            });
            validateCurrentStep();
        };
        
        form.querySelectorAll('.next-btn').forEach(button => {
            button.addEventListener('click', () => { if (currentStep < steps.length) goToStep(currentStep + 1); });
        });

        form.querySelectorAll('.back-btn').forEach(button => {
            button.addEventListener('click', () => { if (currentStep > 1) goToStep(currentStep - 1); });
        });

        planSelectCards.forEach(card => {
            card.addEventListener('click', () => {
                planSelectCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                planInput.value = card.dataset.plan;
                updateDynamicFields();
                validateCurrentStep();
            });
        });

        function updateDynamicFields() {
            const selectedPlan = planInput.value;
            const minLength = 100;
            
            // PayPay関連のロジックは削除

            conceptText.removeAttribute('minlength');
            if (selectedPlan.includes('Creator')) {
                conceptText.setAttribute('minlength', minLength);
                updateCharCounter();
            } else { // Friend Plan, Friend+ Plan
                charCounter.textContent = '文字数制限なし';
            }
        }
        
        function validateCurrentStep() {
            let isValid = false;
            const stepContent = steps[currentStep - 1];
            if (!stepContent) return;
            const nextBtn = stepContent.querySelector('.next-btn');
            const submitBtn = stepContent.querySelector('.submit-btn');
            
            if (currentStep === 1) {
                isValid = planInput.value !== '';
            } else if (currentStep === 2) {
                isValid = mcidInput.checkValidity() && discordInput.checkValidity();
            } else if (currentStep === 3) {
                const minLength = conceptText.hasAttribute('minlength') ? parseInt(conceptText.getAttribute('minlength')) : 0;
                isValid = conceptText.value.length >= minLength && termsAgree.checked;
            }

            if (nextBtn) nextBtn.disabled = !isValid;
            if (submitBtn) submitBtn.disabled = !isValid;
        }

        function updateCharCounter() {
            if (!conceptText.hasAttribute('minlength')) return;
            const minLength = 100;
            const currentLength = conceptText.value.length;
            charCounter.textContent = `${currentLength} / ${minLength} 文字以上`;
            charCounter.style.color = currentLength >= minLength ? '#4ade80' : '#aaa';
        }

        [mcidInput, discordInput, conceptText, termsAgree].forEach(input => {
            if(input) {
                input.addEventListener('input', validateCurrentStep);
                if(input.type === 'textarea') input.addEventListener('input', updateCharCounter);
            }
        });

        if(openModalBtn){
             openModalBtn.addEventListener('click', () => {
                goToStep(1);
                form.reset();
                planSelectCards.forEach(c => c.classList.remove('selected'));
                updateDynamicFields();
                validateCurrentStep();
             });
        }
    }

    // Load Terms and Conditions
    const termsContent = document.getElementById('terms-content');
    if (termsContent) {
        fetch('terms.html')
            .then(response => response.ok ? response.text() : Promise.reject('Failed to load'))
            .then(data => { termsContent.innerHTML = data; })
            .catch(error => { console.error('Terms load error:', error); termsContent.innerHTML = '<p>利用規約の読み込みに失敗しました。</p>'; });
    }
});
