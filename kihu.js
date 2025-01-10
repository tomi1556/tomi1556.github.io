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
    const errorMessage = document.getElementById('error-message');
    const amazonInput = document.getElementById('amazon-code');
    const paypayLinkInput = document.getElementById('paypay-link');
    const mcidInput = document.getElementById('mcid');
    const discordIdInput = document.getElementById('discord-id');
    const donationButtons = document.querySelectorAll('.donation-btn');
    let selectedDonationPlan = null;

    // === 寄付プラン名の定義 ===
    const donationPlans = {
        'amount-100': '有効期限の延長',
        'amount-500': 'ライト',
        'amount-2500': 'スタンダード',
        'amount-5000': 'プレミアム'
    };

    // === フォーム送信 ===
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 入力値の取得
        const mcid = mcidInput.value.trim();
        const discordId = discordIdInput.value.trim();
        const paypayLink = paypayLinkInput.value.trim();
        const amazonCode = amazonInput.value.trim();

        // 必須項目の検証
        if (!mcid || !discordId) {
            errorMessage.textContent = 'Minecraft ID と Discord ID は必須項目です。両方を入力してください。';
            errorMessage.classList.remove('hidden');
            errorMessage.classList.add('show-error');  // アニメーション追加
            successMessage.classList.add('hidden');
            return;
        }

        // 寄付プランの選択確認
        if (!selectedDonationPlan) {
            errorMessage.textContent = '寄付プランを選択してください。';
            errorMessage.classList.remove('hidden');
            errorMessage.classList.add('show-error');
            successMessage.classList.add('hidden');
            return;
        }

        // エディション選択確認（未選択で送信できないように）
        if (!versionField.value) {
            errorMessage.textContent = '機種を選択してください。';
            errorMessage.classList.remove('hidden');
            errorMessage.classList.add('show-error');
            successMessage.classList.add('hidden');
            return;
        }

        // Webhookデータ作成
        const webhookData = {
            embeds: [{
                title: "🎁 新しい寄付がありました！",
                color: 5763719, // 緑色
                fields: [
                    { name: "🆔 Minecraft ID", value: mcid, inline: true },
                    { name: "💬 Discord ID", value: discordId, inline: true },
                    { name: "🎮 エディション", value: versionField.value, inline: true },
                    { name: "💵 寄付プラン", value: selectedPlanName, inline: true },
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

        // GitHub Actionsをトリガー
        triggerGitHubActions(webhookData);
    });
});

// GitHub Actionsをトリガーする関数
function triggerGitHubActions(webhookData) {
    fetch('https://api.github.com/repos/tomi1556/your-repo/actions/workflows/send-webhook.yml/dispatches', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,  // GitHubのアクセストークンはシークレット環境変数から取得
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "ref": "main",  // 使用するブランチを指定（例: mainブランチ）
            "inputs": {
                "webhookData": JSON.stringify(webhookData)  // WebhookデータをGitHub Actionsに渡す
            }
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}
