document.addEventListener('DOMContentLoaded', function() {
    // Page Loader Logic
    const loader = document.getElementById('loader');
    window.addEventListener('load', () => {
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

    // Progress Bar (Donut Chart) Update Function
    function updateProgressBars() {
        const friendAvailable = parseInt(document.getElementById('friend-slots-available').textContent);
        const friendTotal = 3;
        const friendRing = document.getElementById('friend-progress-ring');
        setRingProgress(friendRing, friendAvailable / friendTotal);

        const creatorAvailable = parseInt(document.getElementById('creator-slots-available').textContent);
        const creatorTotal = 5;
        const creatorRing = document.getElementById('creator-progress-ring');
        setRingProgress(creatorRing, creatorAvailable / creatorTotal);
    }
    function setRingProgress(ring, percent) {
        if (!ring) return;
        const radius = ring.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        ring.style.strokeDasharray = `${circumference} ${circumference}`;
        const offset = circumference - (percent * circumference);
        ring.style.strokeDashoffset = offset;
    }
    
    // Multi-Step Form Logic
    const form = document.getElementById('apply-form');
    const steps = [...form.querySelectorAll('.form-step')];
    const stepperItems = [...form.querySelectorAll('.step')];
    const stepLines = [...form.querySelectorAll('.step-line')];
    const nextButtons = [...form.querySelectorAll('.next-btn')];
    const backButtons = [...form.querySelectorAll('.back-btn')];
    const planSelectCards = [...form.querySelectorAll('.plan-select-card')];
    const planInput = document.getElementById('plan-input');
    const mcidInput = document.getElementById('mcid');
    const discordInput = document.getElementById('discord-id');
    const paypayField = document.getElementById('paypay-field');
    const paypayInput = document.getElementById('paypay-link');
    const conceptText = document.getElementById('concept-text');
    const charCounter = document.getElementById('char-counter');
    const termsAgree = document.getElementById('terms-agree');
    const submitButton = form.querySelector('.submit-btn');
    
    let currentStep = 1;

    const updateFormState = () => {
        steps.forEach(step => {
            step.classList.toggle('active', parseInt(step.dataset.step) === currentStep);
        });
        stepperItems.forEach((step, index) => {
            step.classList.toggle('active', index < currentStep);
        });
        validateStep(currentStep);
    };

    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep < steps.length) {
                currentStep++;
                updateFormState();
            }
        });
    });

    backButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateFormState();
            }
        });
    });

    planSelectCards.forEach(card => {
        card.addEventListener('click', () => {
            planSelectCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            planInput.value = card.dataset.plan;
            updateDynamicFields();
            validateStep(1);
        });
    });

    function updateDynamicFields() {
        const selectedPlan = planInput.value;
        const minLength = 100;
        
        paypayField.style.display = selectedPlan === '8G Creator Plan' ? 'block' : 'none';
        paypayInput.required = selectedPlan === '8G Creator Plan';

        conceptText.removeAttribute('minlength');
        if (selectedPlan === 'Friend Plan') {
            charCounter.textContent = '文字数制限なし';
            charCounter.style.color = '#aaa';
        } else if (selectedPlan) {
            conceptText.setAttribute('minlength', minLength);
            const currentLength = conceptText.value.length;
            charCounter.textContent = `${currentLength} / ${minLength} 文字以上`;
        }
    }
    
    function validateStep(stepNumber) {
        let isValid = false;
        const nextBtn = steps[stepNumber - 1].querySelector('.next-btn');
        
        if (stepNumber === 1) {
            isValid = planInput.value !== '';
        } else if (stepNumber === 2) {
            isValid = mcidInput.value.trim() !== '' && discordInput.value.trim() !== '';
            if (paypayInput.required) {
                isValid = isValid && paypayInput.value.trim() !== '' && paypayInput.checkValidity();
            }
        } else if (stepNumber === 3) {
            const minLength = conceptText.hasAttribute('minlength') ? parseInt(conceptText.getAttribute('minlength')) : 0;
            isValid = conceptText.value.length >= minLength && termsAgree.checked;
            if(submitButton) submitButton.disabled = !isValid;
        }

        if (nextBtn) nextBtn.disabled = !isValid;
    }

    [mcidInput, discordInput, paypayInput, conceptText, termsAgree].forEach(input => {
        input.addEventListener('input', () => validateStep(currentStep));
        input.addEventListener('change', () => validateStep(currentStep));
    });
    
    // Load Terms and Conditions
    const termsContent = document.getElementById('terms-content');
    if (termsContent) {
        fetch('terms.html')
            .then(response => response.ok ? response.text() : Promise.reject('Failed to load'))
            .then(data => { termsContent.innerHTML = data; })
            .catch(error => { console.error('Terms load error:', error); termsContent.innerHTML = '<p>利用規約の読み込みに失敗しました。</p>'; });
    }
});
