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

    // === 寄付プラン選択 ===
    donationButtons.forEach(button => {
        button.addEventListener('click', () => {
            donationButtons.forEach(btn => btn.classList.remove('selected')); // 全てのボタンから selected を削除
            button.classList.add('selected'); // クリックしたボタンを選択状態に

            // 寄付プランを設定
            selectedDonationPlan = button.id;
        });
    });

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

        // PayPayリンクの検証 (PayPay選択時)
        if (paypayBtn.classList.contains('selected')) {
            if (!paypayLink) {
                errorMessage.textContent = 'PayPayリンクを入力してください。リンクの形式が間違っていないか確認してください。';
                errorMessage.classList.remove('hidden');
                errorMessage.classList.add('show-error');
                successMessage.classList.add('hidden');
                return;
            }
            const paypayRegex = /^https:\/\/pay\.paypay\.ne\.jp\/.+/;
            if (!paypayRegex.test(paypayLink)) {
                errorMessage.textContent = 'PayPayリンクが正しくありません。';
                errorMessage.classList.remove('hidden');
                errorMessage.classList.add('show-error');
                successMessage.classList.add('hidden');
                return;
            }
        }

        // Amazonギフト券コードの検証 (Amazon選択時)
        if (amazonBtn.classList.contains('selected')) {
            if (!amazonCode) {
                errorMessage.textContent = 'Amazonギフト券コードを入力してください。';
                errorMessage.classList.remove('hidden');
                errorMessage.classList.add('show-error');
                successMessage.classList.add('hidden');
                return;
            }
            const amazonRegex = /^[A-Z0-9]{14,17}$/;
            if (!amazonRegex.test(amazonCode)) {
                errorMessage.textContent = 'Amazonギフト券コードが正しくありません。';
                errorMessage.classList.remove('hidden');
                errorMessage.classList.add('show-error');
                successMessage.classList.add('hidden');
                return;
            }
        }

        // 寄付プラン名を取得
        const selectedPlanName = donationPlans[selectedDonationPlan];

// Expressを使用した例
const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = 3000;

// シークレット（Webhook URL）を環境変数に設定しておく
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

app.use(express.json());

app.post('/send-webhook', (req, res) => {
  const { mcid, discordId, version, planName, paypayLink, amazonCode } = req.body;

  // Webhookデータ作成
  const webhookData = {
    embeds: [{
      title: "🎁 新しい寄付がありました！",
      color: 5763719, // 緑色
      fields: [
        { name: "🆔 Minecraft ID", value: mcid, inline: true },
        { name: "💬 Discord ID", value: discordId, inline: true },
        { name: "🎮 エディション", value: version, inline: true },
        { name: "💵 寄付プラン", value: planName, inline: true },
        ...(paypayLink ? [{ name: "🔗 PayPayリンク", value: paypayLink }] : []),
        ...(amazonCode ? [{ name: "🎟️ Amazonギフト券コード", value: amazonCode }] : [])
      ],
      footer: { text: "🎉 ご支援ありがとうございます！" },
      timestamp: new Date().toISOString()
    }]
  };

  // Webhook送信
  fetch(DISCORD_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(webhookData)
  })
    .then(response => response.json())
    .then(data => {
      res.status(200).json({ success: true, data });
    })
    .catch(error => {
      res.status(500).json({ success: false, error: error.message });
    });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

