# 🧠 MiniMax Daily

**MiniMax Code デイリーサインイン · OAuth トークン更新 · 単一ファイル実行**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · **日本語** · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

> **L0NE-6 オリジナルメンテナンス** · バージョン：**v1.0.0**（2026-11-23）

## 利用範囲

公式リポジトリと Release アセットは無料です。有料販売、内部版や独占版としての再パッケージ、著作権表示の削除、作者名や寄付 QR コードを使った公式認可の偽装は禁止です。詳細は [NOTICE.md](../NOTICE.md) を参照してください。

## 機能

MiniMax Code の Shared MCode OAuth 認証ファイルを読み、アクセストークンの期限が近い場合に更新し、当日のサインイン状態を確認します。サーバーが受取可能と返した場合だけ claim を送信します。旧クライアント向けの leveldb JWT 経路も維持しています。

メイン処理は Python 標準ライブラリのみを使用し、Python 3.8 以降に対応します。

## クイックスタート

1. MiniMax Code デスクトップクライアントでログインします。
2. 通常は `~/.minimax/auth/prod/cn/mcode-public/auth.json` にある OAuth ファイルを確認します。
3. 次のコマンドを実行します。

```bash
python minimax_daily.py status
python minimax_daily.py auto
```

更新された認証情報は同じファイルへアトミックに書き戻されます。実行ユーザーに読み書き権限が必要です。

## Qinglong

1. `minimax_daily.py` をアップロードします。
2. `auth.json` を非公開の永続ディレクトリへ配置します。
3. `MINIMAX_OAUTH_AUTH_FILE` をそのファイルへ設定します。
4. タスクコマンドを `task minimax_daily.py auto` にします。
5. 毎日 1 回、例えば `17 7 * * *` で十分です。

## GitHub Actions

ワークフローは [`.github/workflows/minimax.yml`](../.github/workflows/minimax.yml) です。

- `main` への push：単体テスト、コンパイル確認、Ruff を実行します。
- `workflow_dispatch`：`MINIMAX_AUTH_JSON` を `$RUNNER_TEMP/auth.json` に書き込み、`python minimax_daily.py auto` を実行します。

| Secret | 必須 | 内容 |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | 手動実行時に必須 | MiniMax `auth.json` の完全な JSON |

公開リポジトリではローテーション後の Token を永続化しません。ワークフローは `auth.json` を commit、upload、保存せず、現在の Runner の一時領域だけを使用します。実行中に Refresh Token がローテーションされた場合、新しい値はジョブ終了時に失われるため、次回は Secret の更新が必要になることがあります。

## 環境変数

| 変数 | 必須 | 説明 |
| :--- | :---: | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | 条件付き | 新版 OAuth `auth.json` のパス。 |
| `MINIMAX_LS_LEVELDB` | 任意 | 旧版 leveldb ディレクトリの上書き。 |
| `MINIMAX_DESKTOP_VERSION` | 任意 | リクエストヘッダーのデスクトップ版。既定値は `3.1.6`。 |

## CLI

| コマンド | 動作 |
| :--- | :--- |
| `python minimax_daily.py auto` | 状態確認後、受取可能ならサインインします。 |
| `python minimax_daily.py status` | 読み取り専用の状態確認です。 |
| `python minimax_daily.py login` | Device Flow を開始し、ブラウザ確認を待ちます。 |

## 成功条件

| 結果 | 意味 | 終了コード |
| :--- | :--- | :---: |
| `CLAIMED` | `claim_result=1` で受取成功。 | 0 |
| `ALREADY` | 当日受取済み、または冪等な `claim_result=2`。 | 0 |
| `PENDING` | 状態確認で受取可能、claim は未送信。 | 0 |
| `INACTIVE` | 当日の有効な項目なし。 | 0 |
| `NO_SESSION` | ログイン状態が無効。 | 1 |
| `NETWORK` | 通信失敗。 | 1 |
| `NO_AUTH` | 認証情報が見つからない。 | 2 |
| `ERROR` | API、JSON、引数、実行時エラー。 | 1 または 2 |

HTTP 200 だけでは成功ではありません。サーバーの状態、claim 応答、ポイント、連続日数を確認します。

## プライバシーと免責

リポジトリにアカウント、電話番号、Token、JWT、端末情報は含まれません。スクリプトは認証情報の値を出力しません。Issue に `auth.json`、Cookie、認証済み通信の完全なログを貼らないでください。

本プロジェクトは MiniMax 公式とは関係せず、承認も受けていません。API は変更される可能性があります。利用条件を守り、自己責任で使用してください。

## サポート

<p align="center">
  <img src="../assets/donate-wechat.png" width="220" alt="WeChat 投げ銭 QR" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../assets/donate-alipay.jpg" width="220" alt="Alipay 投げ銭 QR" />
</p>

QR コードは作者への任意の投げ銭用です。第三者がダウンロード、導入代行、内部版、会員グループなどの名目で料金を請求する行為は作者と無関係です。

## Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>
