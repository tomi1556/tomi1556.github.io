document.addEventListener('DOMContentLoaded', () => {
    const paypayBtn = document.getElementById('paypay-btn');
    const amazonBtn = document.getElementById('amazon-btn');
    const paypaySection = document.getElementById('paypay-section');
    const amazonSection = document.getElementById('amazon-section');
    const form = document.getElementById('donation-form');
    const successMessage = document.getElementById('success-message');
    const amazonInput = document.getElementById('amazon-code');
    const paypayLinkInput = document.getElementById('paypay-link');
    const versionField = document.getElementById('version');
    const javaBtn = document.getElementById('java-btn');
    const bedrockBtn = document.getElementById('bedrock-btn');

    // 初期状態でAmazonが選択された状態にする
    amazonSection.classList.remove('hidden');
    paypaySection.classList.add('hidden');
    amazonBtn.classList.add('selected');  // 初期状態でAmazonを選択

    // PayPayボタンのクリックイベント
    paypayBtn.addEventListener('click', () => {
        paypaySection.classList.remove('hidden');
        amazonSection.classList.add('hidden');
        paypayBtn.classList.add('selected');
        amazonBtn.classList.remove('selected');
    });

    // Amazonボタンのクリックイベント
    amazonBtn.addEventListener('click', () => {
        amazonSection.classList.remove('hidden');
        paypaySection.classList.add('hidden');
        amazonBtn.classList.add('selected');
        paypayBtn.classList.remove('selected');
    });

    // Minecraftバージョン選択のクリックイベント
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

    // フォーム送信イベント
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 入力値を取得
        const paypayLink = paypayLinkInput.value.trim();
        const amazonCode = amazonInput.value.trim();
        const mcid = document.getElementById('mcid').value;

        let sendData = ''; // Webhookに送信するデータ

        // PayPayリンクが正しいかを検証 (PayPayが選ばれている時)
        if (paypayBtn.classList.contains('selected') && paypayLink) {
            const paypayRegex = /^https:\/\/pay\.paypay\.ne\.jp\/.+/;
            if (paypayRegex.test(paypayLink)) {
                sendData += `PayPayリンク: ${paypayLink}\n`;  // 正しい場合PayPayリンクを送信
            } else {
                alert('PayPayリンクが正しくありません');
                return;
            }
        }

        // Amazonギフト券コードが正しいかを検証 (Amazonが選ばれている時)
        if (amazonBtn.classList.contains('selected') && amazonCode) {
            const amazonRegex = /^[A-Z0-9]{14,17}$/;  // ハイフンなし、17文字
            if (amazonRegex.test(amazonCode)) {
                sendData += `Amazonコード: ${amazonCode}\n`;  // 正しい場合Amazonコードを送信
            } else {
                alert('Amazonギフト券コードが正しくありません');
                return;
            }
        }

        // 片方が空でも送信できるようにする
        if (sendData === '') {
            alert('PayPayリンクまたはAmazonコードのいずれかを入力してください');
            return;
        }

        // Webhookにデータを送信
        fetch('YOUR_WEBHOOK_URL', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: `Minecraft ID: ${mcid}\n${sendData}`
            })
        });

        // 成功メッセージの表示
        successMessage.classList.remove('hidden');
    });
});
