document.addEventListener('DOMContentLoaded', () => {
    const versionField = document.getElementById('version');
    const javaBtn = document.getElementById('java-btn');
    const bedrockBtn = document.getElementById('bedrock-btn');
    const amazonBtn = document.getElementById('amazon-btn');
    const paypayBtn = document.getElementById('paypay-btn');
    const amazonCodeSection = document.getElementById('amazon-code-section');
    const paypayLinkSection = document.getElementById('paypay-link-section');
    const form = document.getElementById('donation-form');
    const successMessage = document.getElementById('success-message');

    let selectedPaymentMethod = '';

    javaBtn.onclick = () => {
        versionField.value = 'Java版';
        javaBtn.classList.add('selected');
        bedrockBtn.classList.remove('selected');
    };

    bedrockBtn.onclick = () => {
        versionField.value = '統合版';
        bedrockBtn.classList.add('selected');
        javaBtn.classList.remove('selected');
    };

    amazonBtn.onclick = () => {
        selectedPaymentMethod = 'Amazonギフト券';
        amazonCodeSection.classList.remove('hidden');
        paypayLinkSection.classList.add('hidden');
    };

    paypayBtn.onclick = () => {
        selectedPaymentMethod = 'PayPay';
        paypayLinkSection.classList.remove('hidden');
        amazonCodeSection.classList.add('hidden');
    };

    form.onsubmit = (e) => {
        e.preventDefault();
        const mcid = document.getElementById('mcid').value;
        const amount = document.getElementById('donation-amount').value;

        fetch('YOUR_WEBHOOK_URL', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mcid,
                amount,
                paymentMethod: selectedPaymentMethod,
                version: versionField.value
            })
        }).then(() => {
            successMessage.classList.remove('hidden');
        }).catch(() => {
            alert('送信に失敗しました');
        });
    };
});
