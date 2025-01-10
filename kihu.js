        // 寄付プラン名を取得
        const selectedPlanName = donationPlans[selectedDonationPlan];

        // === Webhookデータ作成 ===
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

        // === Webhook送信 ===
        fetch('https://discord.com/api/webhooks/1327163439214235752/o4y_-xIkEjUDPfgjGtM157Z0ruBxwveodFfq0MczjKL7e3veMZvelanb7AQSlHXLMrrz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(webhookData)
        }).then(() => {
            // 成功メッセージの表示
            successMessage.textContent = '送金が確認されました！ありがとうございます！';
            successMessage.classList.remove('hidden');
            successMessage.classList.add('show-success');  // アニメーション追加
            errorMessage.classList.add('hidden');
            form.reset();
            versionField.value = '';  // フォームのリセット
            selectedDonationPlan = null; // 寄付プランのリセット
        }).catch(() => {
            alert('送信に失敗しました');
        });
    });
});
