document.addEventListener('DOMContentLoaded', () => {
    const javaBtn = document.getElementById('java-btn');
    const bedrockBtn = document.getElementById('bedrock-btn');
    const amazonBtn = document.getElementById('amazon-btn');
    const paypayBtn = document.getElementById('paypay-btn');
    const form = document.getElementById('donation-form');
    const successMessage = document.getElementById('success-message');
    const versionField = document.getElementById('version');
    const amountField = document.getElementById('donation-amount');
    const codeField = document.getElementById('code-input');
    const paypayLinkField = document.getElementById('paypay-link');

    let selectedPaymentMethod = '';

    // バージョン選択
    javaBtn.addEventListener('click', () => {
        versionField.value = 'Java版';
        javaBtn.classList.add('selected');
        bedrockBtn.classList.remove('selected');
    });

    bedrockBtn.addEventListener('click', () => {
        versionField.value = '統合版';
        bedrockBtn.classList.add('selected');
        javaBtn.classList.remove('selected');
    });

    // 寄付方法選択
    amazonBtn.addEventListener('click', () => {
        selectedPaymentMethod = 'Amazonギフト券';
        amazonBtn.classList.add('selected');
        paypayBtn.classList.remove('selected');
    });

    paypayBtn.addEventListener('click', () => {
        selectedPaymentMethod = 'PayPay';
        paypayBtn.classList.add('selected');
        amazonBtn.classList.remove('selected');
    });

    // 送信
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const mcid = document.getElementById('mcid').value.trim();
        const amount = amountField.value.trim();

        if (!mcid || !amount || !selectedPaymentMethod) {
            alert('すべての項目を入力してください。');
            return;
        }

        successMessage.classList.remove('hidden');
    });
});
