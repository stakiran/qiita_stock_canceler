# qiita_stock_canceler
Qiita v2 API を使って自身のストックを全て消去する Python スクリプト

# Requirement

- Windows 7+
- Python 3.6
- requests ライブラリ

# Installation

- `git clone https://github.com/stakiran/qiita_stock_canceler`
- `cd qiita_stock_canceler`
- `copy stock_canceler.bat.sample stock_canceler.bat`
- `stock_canceler.bat` 内の以下を編集する
  - QIITA_ACCESS_TOKEN 環境変数にアクセストークンを設定する
    - アクセストークンは [Qiitaにログイン後、設定画面から発行できます](https://qiita.com/settings/applications)
    - **read_qiita** と **write_qiita** の二つが必要です
  - QIITA_USERNAME 環境変数に自分の Qiita ユーザー名を指定する
- プロキシが必要なら HTTPS_PROXY 環境変数もセットする
  - 例: `set HTTPS_PROXY=https://(IP):(PORT)`
- `stock_canceler.bat` を実行する

# Demo

当方の Qiita アカウントで実行してみた例です。655件のストックを消去しています。

```
$ python stock_canceler.py -u sta
getting between 1 to 100...
getting between 101 to 200...
getting between 201 to 300...
getting between 301 to 400...
getting between 401 to 500...
getting between 501 to 600...
getting between 601 to 700...
1/655 TITLE:Windows環境＋node.js＋mocha＋istanbulでUTしてコードカバレッジを取る...
2/655 TITLE:grunt+istanbul+mochaでNode.jsのテスト＆カバレッジ計測を行う...
3/655 TITLE:システムで「性別」の情報を扱う前に知っておくべきこと...
...
653/655 TITLE:2015年センター試験数学IAを全てプログラム(Python)で解く...
654/655 TITLE:100万倍速いプログラムを書く...
655/655 TITLE:いい結婚相手を見つける最適な方法を検証してみた...
Fin.

$ python stock_canceler.py -u sta
getting between 1 to 100...
Fin.
```

# 注意事項

ストック消去は 1 件につき 1 リクエストを消費するため、ストック数が多い場合は **Rate Limit を使い切らないよう** ご注意ください。Qiita API v2 の Rate Limit は 2018/04/13 現在で [1000リクエスト/時](https://qiita.com/api/v2/docs#%E5%88%A9%E7%94%A8%E5%88%B6%E9%99%90) です。

# License

[MIT License](LICENSE)

# Author

[stakiran](https://github.com/stakiran)
