# LogAggregation
NGINXのアクセスログを集計してWebhookへポスト

# 使い方
Nginxのアクセスログを`fluent/fluentd:v1.16-1`を用いてMySQLに登録するシステムを作っておきます。

そのMySQLサーバーに向けてsqlalchemyを接続しましょう。

# 変更歴
## 2024-01-29
* 初期作成