# discord_cost_check
AWSの月間コスト算出結果をDiscordに通知します

（README作成中）

【discord】<br>
webhookURLを作成します

【AWS】<br>
Lambda関数：discord_cost_check_lambda.py<br>
　→web_hookのurlは置き換えてください。<br>
EventBridgeルール：discord_cost_check_event.json<br>
　→7日間ごとに実行します。Targetは置き換えてください。<br>

## 出力イメージ
![出力イメージ](image2.jpg)
