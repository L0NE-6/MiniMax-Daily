# 🧠 MiniMax Daily

**MiniMax Code daily sign-in · OAuth token refresh · single-file runner**

[简体中文](../README.md) · **English** · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

> **Originally maintained by L0NE-6** · Version: **v1.0.0** (2026-11-23)

## Usage boundary

The official repository and release assets are free. Do not resell, paywall, repackage as an internal or exclusive edition, remove copyright notices, or use the author's identity and donation QR codes to imply official authorization. See [NOTICE.md](../NOTICE.md).

## What it does

This project reads the MiniMax Code Shared MCode OAuth credential file, refreshes an expiring access token, queries today's sign-in status, and claims the reward only when the server says it is available. A legacy leveldb JWT path is retained for older clients.

The main flow uses only the Python standard library and supports Python 3.8 or newer.

## Quick start

1. Sign in with the MiniMax Code desktop client.
2. Locate the OAuth file, normally `~/.minimax/auth/prod/cn/mcode-public/auth.json`.
3. Run:

```bash
python minimax_daily.py status
python minimax_daily.py auto
```

The script writes a refreshed credential back to the same file. The file must be readable and writable by the runtime account.

## Qinglong

1. Upload `minimax_daily.py`.
2. Put `auth.json` in a private, persistent directory.
3. Set `MINIMAX_OAUTH_AUTH_FILE` to that file.
4. Create a task with `task minimax_daily.py auto`.
5. A daily schedule such as `17 7 * * *` is sufficient.

## GitHub Actions

The workflow is [`.github/workflows/minimax.yml`](../.github/workflows/minimax.yml).

- Pushes to `main` run unit tests, compile checks, and Ruff.
- `workflow_dispatch` writes the `MINIMAX_AUTH_JSON` secret to `$RUNNER_TEMP/auth.json` and runs `python minimax_daily.py auto`.

### Secret

| Name | Required | Value |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | Yes for manual runs | Full JSON contents of MiniMax `auth.json` |

### Public repository token policy

The workflow never commits, uploads, or otherwise persists `auth.json` or a rotated Refresh Token. The file exists only in `RUNNER_TEMP` for the current job. If a run rotates the Refresh Token, the new value is lost when the job ends, so a later run may need an updated Secret. v1.0.0 intentionally does not commit credentials back to a public repository.

## Environment variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | Conditional | Path to the current MiniMax OAuth `auth.json`. |
| `MINIMAX_LS_LEVELDB` | Optional | Legacy MiniMax leveldb directory override. |
| `MINIMAX_DESKTOP_VERSION` | Optional | Desktop version used in request headers; default `3.1.6`. |

## CLI

| Command | Behavior |
| :--- | :--- |
| `python minimax_daily.py auto` | Query and claim if available. |
| `python minimax_daily.py status` | Read-only status check. |
| `python minimax_daily.py login` | Start Device Flow and wait for browser confirmation. |

## Success criteria

| Result | Meaning | Exit code |
| :--- | :--- | :---: |
| `CLAIMED` | `claim_result=1`; the reward was claimed. | 0 |
| `ALREADY` | Today's reward was already claimed, including idempotent `claim_result=2`. | 0 |
| `PENDING` | Status mode confirms the reward is available; no claim was sent. | 0 |
| `INACTIVE` | No active or claimable item today. | 0 |
| `NO_SESSION` | The login session is invalid. | 1 |
| `NETWORK` | The network request failed. | 1 |
| `NO_AUTH` | No OAuth or legacy JWT credential was found. | 2 |
| `ERROR` | API, JSON, parameter, or runtime error. | 1 or 2 |

An HTTP 200 response alone is not success. The server status, claim result, points, and streak data are the acceptance evidence.

## Privacy

The repository contains no account, phone number, token, JWT, or device data. Credentials stay in the injected file. The script does not print token values. Never post `auth.json`, cookies, or raw authenticated traffic in an issue.

## Disclaimer

MiniMax may change its OAuth or sign-in protocol at any time. This independent project is not affiliated with or endorsed by MiniMax. Use it only in accordance with the applicable service terms and at your own risk.

## Support

<p align="center">
  <img src="../assets/donate-wechat.png" width="220" alt="WeChat donation QR code" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../assets/donate-alipay.jpg" width="220" alt="Alipay donation QR code" />
</p>

The QR codes are only for voluntary tips to the author. Third-party charges for downloads, deployment, private editions, or membership access are not authorized.

## Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>
