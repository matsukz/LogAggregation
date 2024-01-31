# LogAggregation
NGINXのアクセスログを集計してWebhookへポスト

# 使い方
Nginxのアクセスログを`fluent/fluentd:v1.16-1`を用いてMySQLに登録するシステムを作っておきます。

https://github.com/matsukz/NginxLog-MySQL

そのMySQLサーバーに向けてsqlalchemyを接続しましょう。

* 実行前にネットワークを作成しましょう
```bash
docker network create --driver bridge --opt com.docker.network.driver.mtu=1420 NginxLog
```

# 定期実行
```bash
$ crontab -e
```

```bash
#毎日0:10に実行(たぶん)
10 0  * * * /usr/local/bin/docker-compose -f ~/LogAggregation/docker-compose.yml up -d
```

# 変更歴
## 2024-01-29
* 初期作成

## 2024-01-30
* 仮完成
* docker networkをまとめた
