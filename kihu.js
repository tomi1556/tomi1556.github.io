document.addEventListener('DOMContentLoaded', () => {
    // === DOM要素の取得 ===
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
    const donationButtons = document.querySelectorAll('.donation-btn');

    // === 初期設定 ===
    versionField.value = ''; // エディションは未選択状態
    javaBtn.classList.remove('selected');
    bedrockBtn.classList.remove('selected');
    amazonSection.classList.remove('hidden');
    paypaySection.classList.add('hidden');
    amazonBtn.classList.add('selected');

    // === エディション選択 ===
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

    // === 寄付方法選択 ===
    paypayBtn.addEventListener('click', () => {
        paypaySection.classList.remove('hidden');
        amazonSection.classList.add('hidden');
        paypayBtn.classList.add('selected');
        amazonBtn.classList.remove('selected');
    });

    amazonBtn.addEventListener('click', () => {
        amazonSection.classList.remove('hidden');
        paypaySection.classList.add('hidden');
        amazonBtn.classList.add('selected');
        paypayBtn.classList.remove('selected');
    });

    // === 金額選択 ===
    donationButtons.forEach(button => {
        button.addEventListener('click', () => {
            donationButtons.forEach(btn => btn.classList.remove('selected')); // 全てのボタンから selected を削除
            button.classList.add('selected'); // クリックしたボタンを選択状態に

            // 寄付金額を設定
            switch (button.id) {
                case 'amount-100':
                    donationAmountInput.value = '100';
                    break;
                case 'amount-500':
                    donationAmountInput.value = '500';
                    break;
                case 'amount-2500':
                    donationAmountInput.value = '2500';
                    break;
                case 'amount-5000':
                    donationAmountInput.value = '5000';
                    break;
            }
        });
    });

    // === フォーム送信 ===
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 入力値の取得
        const mcid = mcidInput.value.trim();
        const discordId = discordIdInput.value.trim();
        const donationAmount = donationAmountInput.value.trim();
        const paypayLink = paypayLinkInput.value.trim();
        const amazonCode = amazonInput.value.trim();

        // 必須項目の検証
        if (!mcid || !discordId || !donationAmount) {
            alert('Minecraft ID、Discord ID、金額は必須項目です');
            return;
        }

        // エディション選択確認（未選択で送信できないように）
        if (!versionField.value) {
            alert('エディションを選択してください');
            return;
        }

        // PayPayリンクの検証 (PayPay選択時)
        if (paypayBtn.classList.contains('selected')) {
            if (!paypayLink) {
                alert('PayPayリンクを入力してください');
                return;
            }
            const paypayRegex = /^https:\/\/pay\.paypay\.ne\.jp\/.+/;
            if (!paypayRegex.test(paypayLink)) {
                alert('PayPayリンクが正しくありません');
                return;
            }
        }

        // Amazonギフト券コードの検証 (Amazon選択時)
        if (amazonBtn.classList.contains('selected')) {
            if (!amazonCode) {
                alert('Amazonギフト券コードを入力してください');
                return;
            }
            const amazonRegex = /^[A-Z0-9]{14,17}$/;
            if (!amazonRegex.test(amazonCode)) {
                alert('Amazonギフト券コードが正しくありません');
                return;
            }
        }

        // === Webhookデータ作成 ===
        const webhookData = {
            embeds: [{
                title: "🎁 新しい寄付がありました！",
                color: 5763719, // 緑色
                fields: [
                    { name: "🆔 Minecraft ID", value: mcid, inline: true },
                    { name: "💬 Discord ID", value: discordId, inline: true },
                    { name: "🎮 エディション", value: versionField.value, inline: true },
                    { name: "💵 寄付金額", value: `¥${donationAmount}`, inline: true },
                    ...(paypayBtn.classList.contains('selected') ? [{
                        name: "🔗 PayPayリンク", value: paypayLink
                    }] : []),
                    ...(amazonBtn.classList.contains('selected') ? [{
                        name: "🎟️ Amazonギフト券コード", value: amazonCode
                    }] : [])
                ],
                footer: { text: "🎉 ご支援ありがとうございます！" },
                timestamp: new Date().toISOString()
            }]
        };

        // === Webhook送信 ===
        fetch('https://discord.com/api/webhooks/1321477762338521179/YEvfJJo8opXHNbR4VHLlYEKRLpM1GtOEvKk9YNvZrAGj_l4ehUdkqx8h30bdu4j4d-BK', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(webhookData)
        }).then(() => {
            successMessage.classList.remove('hidden');
            form.reset();
            versionField.value = '';  // フォームのリセット
        }).catch(() => {
            alert('送信に失敗しました');
        });
    });
});
