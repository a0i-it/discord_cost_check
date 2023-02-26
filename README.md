# discord_cost_check
AWSの月間コスト算出結果をDiscordに通知します

【discord側の準備】<br>
+ [公式ドキュメント](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)を参考にWebhookURLを作成します。

【AWS側の準備】<br>
+ Lambda関数：discord_cost_check_lambda.py<br>
   - web_hookのurlは置き換えてください。<br>
   - Lambda実行ロールはCostExplorerの読み取り権限を付与してください。<br>
   - 為替APIは[クジラ外国為替確認API](https://api.aoikujira.com/index.php?fx)を利用させてもらいました。<br>
+ EventBridgeルール：discord_cost_check_event.json<br>
   - 7日間ごとに実行します。Targetは置き換えてください。<br>

## 出力イメージ
![出力イメージ](image2.jpg)
