# 🧠 MiniMax Daily

**MiniMax Code 每日簽到 · OAuth 憑據續期 · 單檔案執行**

[简体中文](../README.md) · [English](README.en.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

> **L0NE-6 原創維護** · 版本：**v1.1.0**（2026-11-24）

`MINIMAX_SITE=cn` 使用國內站；`MINIMAX_SITE=global` 使用
`agent.minimax.io` 與 `account.minimax.io`，兩站權杖不通用。國際版憑據通常位於
`~/.minimax/auth/prod/en/mcode-public/auth.json`。

## 使用邊界

官方倉庫與 Release 資產永久免費。禁止付費包裝、倒賣、搬運引流、刪除版權資訊，或使用作者身分與收款碼製造官方授權假象。詳見 [NOTICE.md](../NOTICE.md)。

## 功能

本專案讀取 MiniMax Code 的 Shared MCode OAuth 憑據，在存取權杖即將過期時自動續期，查詢今日簽到狀態，並只在服務端允許領取時發送 claim。舊版 leveldb JWT 路徑仍保留相容。

主流程只使用 Python 標準庫，支援 Python 3.8 以上版本。

## 快速開始

1. 在 MiniMax Code 桌面端完成登入。
2. 找到 OAuth 檔案：國內版通常位於 `~/.minimax/auth/prod/cn/mcode-public/auth.json`，
   國際版通常位於 `~/.minimax/auth/prod/en/mcode-public/auth.json`。
3. 執行：

```bash
python minimax_daily.py status
python minimax_daily.py auto
```

刷新後的新憑據會原子寫回同一檔案，因此執行帳號必須具有讀寫權限。

## 青龍

1. 上傳 `minimax_daily.py`。
2. 將 `auth.json` 放入私有且持久的目錄。
3. 設定 `MINIMAX_OAUTH_AUTH_FILE` 指向該檔案。
4. 任務命令填 `task minimax_daily.py auto`。
5. 每日一次即可，例如 `17 7 * * *`。

## GitHub Actions

工作流位於 [`.github/workflows/minimax.yml`](../.github/workflows/minimax.yml)。

- Push 到 `main`：執行單元測試、編譯檢查與 Ruff。
- `workflow_dispatch`：將 `MINIMAX_AUTH_JSON` 寫入 `$RUNNER_TEMP/auth.json`，再執行 `python minimax_daily.py auto`。

| Secret | 必填 | 內容 |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | 手動執行時必填 | MiniMax `auth.json` 的完整 JSON |

公開倉庫不持久化輪換 Token。工作流不會提交、上傳或保存 `auth.json`；檔案只存在於當前 Runner 的暫存目錄。若本輪刷新了 Refresh Token，Runner 結束後新值會消失，下一次可能需要更新 Secret。

## 環境變數

| 變數 | 必填 | 說明 |
| :--- | :---: | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | 條件必填 | 新版 OAuth `auth.json` 路徑。 |
| `MINIMAX_LS_LEVELDB` | 可選 | 舊版 leveldb 目錄覆蓋。 |
| `MINIMAX_DESKTOP_VERSION` | 可選 | 請求頭桌面版本，預設 `3.1.6`。 |

## 命令列

| 命令 | 行為 |
| :--- | :--- |
| `python minimax_daily.py auto` | 查詢並在可領時簽到。 |
| `python minimax_daily.py status` | 只查狀態。 |
| `python minimax_daily.py login` | 啟動 Device Flow，等待瀏覽器確認。 |

## 成功判據

| 結果 | 含義 | 退出碼 |
| :--- | :--- | :---: |
| `CLAIMED` | 服務端回傳 `claim_result=1`。 | 0 |
| `ALREADY` | 今日已簽，或冪等回傳 `claim_result=2`。 | 0 |
| `PENDING` | 狀態模式確認可領，但未發 claim。 | 0 |
| `INACTIVE` | 今日沒有可領項目。 | 0 |
| `NO_SESSION` | 登入態失效。 | 1 |
| `NETWORK` | 網路請求失敗。 | 1 |
| `NO_AUTH` | 找不到憑據。 | 2 |
| `ERROR` | 介面、JSON、參數或執行錯誤。 | 1 或 2 |

HTTP 200 不能單獨代表成功，必須以服務端狀態、領取回執、積分與連簽天數為準。

## 隱私與免責

倉庫不含帳號、手機號、Token、JWT 或裝置資訊。腳本不輸出憑據原文。請勿在 Issue 張貼 `auth.json`、Cookie 或完整認證流量。

本專案與 MiniMax 官方無隸屬或背書關係。介面可能隨時變更，請遵守服務條款並自行承擔使用風險。

## 支持

<p align="center">
  <img src="../assets/donate-wechat.png" width="220" alt="微信讚賞碼" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../assets/donate-alipay.jpg" width="220" alt="支付寶收款碼" />
</p>

收款碼僅供自願讚賞。第三方以代下載、代部署、內部版或會員群名義收費，均與作者無關。

## Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>
