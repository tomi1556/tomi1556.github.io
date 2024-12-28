document.addEventListener('DOMContentLoaded', () => {
    // DOM要素の取得
    const versionField = document.getElementById('version');
    const javaBtn = document.getElementById('java-btn');
    const bedrockBtn = document.getElementById('bedrock-btn');
    const amazonBtn = document.getElementById('amazon-btn');
    const paypayBtn = document.getElementById('paypay-btn');
    const paypaySection = document.getElementById('paypay-section');
    const amazonSection = document.getElementById('amazon-section');
    const form = document.getElementById('donation-form');
    const successMessage = document.getElementById('success-message');
    const amazonInput = document.getElementById('amazon-code');
    const paypayLinkInput = document.getElementById('paypay-link');
    const mcidInput = document.getElementById('mcid');
    const discordIdInput = document.getElementById('discord-id');
    const donationAmountInput = document.getElementById('donation-amount');

    // 初期設定: Amazonが選択された状態
    amazonSection.classList.remove('hidden');
    paypaySection.classList.add('hidden');
    amazonBtn.classList.add('selected');  // 初期状態でAmazonを選択

    // Minecraftバージョン選択
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

    // フォーム送信イベント
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 入力値の取得
        const mcid = mcidInput.value;
        const discordId = discordIdInput.value;
        const donationAmount = donationAmountInput.value;
        const paypayLink = paypayLinkInput.value.trim();
        const amazonCode = amazonInput.value.trim();

        let sendData = ''; // Webhookに送信するデータ

        // PayPayリンクの検証 (PayPayが選択されている場合)
        if (paypayBtn.classList.contains('selected') && paypayLink) {
            const paypayRegex = /^https:\/\/pay\.paypay\.ne\.jp\/.+/;
            if (paypayRegex.test(paypayLink)) {
                sendData += `PayPayリンク: ${paypayLink}\n`;  // 正しい場合PayPayリンクを送信
            } else {
                alert('PayPayリンクが正しくありません');
                return;
            }
        }

        // Amazonギフト券コードの検証 (Amazonが選択されている場合)
        if (amazonBtn.classList.contains('selected') && amazonCode) {
            const amazonRegex = /^[A-Z0-9]{14,17}$/;  // ハイフンなし、17文字
            if (amazonRegex.test(amazonCode)) {
                sendData += `Amazonコード: ${amazonCode}\n`;  // 正しい場合Amazonコードを送信
            } else {
                alert('Amazonギフト券コードが正しくありません');
                return;
            }
        }

        // 必要な情報が足りている場合は送信しない
        if (!sendData) {
            alert('PayPayリンクまたはAmazonコードのいずれかを入力してください');
            return;
        }

        // Webhookに送信するデータの作成
        const webhookData = {
            content: `Minecraft ID: ${mcid}\nDiscord ID: ${discordId}\n金額: ¥${donationAmount}\nエディション: ${versionField.value}\n${sendData}`
        };

        // Discord Webhookにデータを送信
        fetch('https://discord.com/api/webhooks/1321477762338521179/YEvfJJo8opXHNbR4VHLlYEKRLpM1GtOEvKk9YNvZrAGj_l4ehUdkqx8h30bdu4j4d-BK', {  // 必ず実際のWebhook URLを挿入してください
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(webhookData)
        }).then(() => {
            // 成功メッセージの表示
            successMessage.classList.remove('hidden');
        }).catch(() => {
            alert('送信に失敗しました');
        });
    });
});
