<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🧠 MiniMax Daily

**MiniMax Code 每日签到 · 凭据自动续期 · 单文件运行 · 青龙与 GitHub Actions 友好**

> **L0NE-6 原创维护** · 当前版本：**v1.0.0**（2026-11-23）

[简体中文](README.md) · [English](docs/README.en.md) · [繁體中文](docs/README.zh-Hant.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [Português (BR)](docs/README.pt-BR.md)

🔐 OAuth 续期 · ♻️ 轮换令牌原子写回 · ✅ 幂等签到 · 📊 中文状态报告 · 🐧 青龙友好 · ☁️ GitHub Actions

<img src="https://img.shields.io/github/v/release/L0NE-6/MiniMax-Daily?style=for-the-badge&label=Release&color=2ea44f&logo=github" />
<img src="https://img.shields.io/github/stars/L0NE-6/MiniMax-Daily?style=for-the-badge&label=Stars&color=FFC75F&logo=github" />
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20%E9%9D%92%E9%BE%99-4EAA25?style=for-the-badge&logo=linux&logoColor=white" />
<img src="https://img.shields.io/badge/Deploy-%E9%9D%92%E9%BE%99%20%7C%20GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-F472B6?style=for-the-badge" />

[✨ 速览](#-30-秒速览) · [🧩 原理](#-工作原理) · [🚀 青龙](#-部署方式一青龙面板) · [☁️ Actions](#-部署方式二github-actions) · [🔧 环境变量](#-环境变量) · [⌨️ CLI](#-命令行-cli) · [✅ 成功判据](#-成功判据) · [🚫 使用边界](#usage-policy) · [✦ 星轨](#-星轨-star-history)

</div>

---

<a id="usage-policy"></a>
## 🚫 使用边界与禁止倒卖

> [!IMPORTANT]
> **官方版本永久免费。** 未经作者书面许可，禁止付费包装、搬运引流、冒充作者，或使用作者身份与二维码制造官方授权假象。

本项目仓库、脚本、部署说明和 Release 下载始终免费公开。未经作者明确书面许可，禁止将本项目包装为付费资源、内部版、独家版、会员权益、收费课程、付费部署或包更新服务；禁止搬运到其他账号、群组、频道、网盘、电商或付费平台进行涨粉、截流、倒卖和引流；禁止删除作者与版权信息后冒充原创；禁止使用作者昵称、头像、二维码和项目名称制造官方授权假象。

仓库中的微信和支付宝二维码仅用于向作者自愿赞赏。任何第三方以下载费、激活费、内部版、代部署费或会员群门槛等名义收费，均与作者无关。完整规则见 [NOTICE.md](NOTICE.md)。

---

## ✨ 30 秒速览

| 维度 | 说明 |
| :--- | :--- |
| **做什么** | 读取 MiniMax Code 登录凭据，自动续期访问令牌，查询签到状态并领取当日积分。 |
| **输入** | MiniMax `auth.json`，或旧版 MiniMax leveldb 目录。 |
| **输出** | 单行 JSON，包含 `CLAIMED`、`ALREADY`、`PENDING`、`NO_SESSION` 等状态，以及积分和连签天数。 |
| **部署** | 青龙面板、GitHub Actions、Windows / Linux 本地运行。 |
| **依赖** | Python 3.8+，主流程仅使用标准库。 |
| **成功判据** | 服务端状态为今日已签，或领取回执明确返回 `claim_result=1/2`；单个 HTTP 200 不算成功。 |

## 🧭 这是什么

这是一个面向 MiniMax Code 桌面端的单文件签到工具。它不会要求你粘贴明文 Token，而是优先读取桌面端生成的 Shared MCode OAuth 凭据文件，在访问令牌临近过期时完成刷新，并把轮换后的新凭据原子写回原文件。

脚本只做三件事：

1. 定位并校验 MiniMax OAuth 凭据。
2. 查询今日签到状态，只有今日可领取时才发送领取请求。
3. 输出可审计的 JSON 结果，不打印 Access Token、Refresh Token 或旧版 JWT。

---

## 🧩 工作原理

### 1. Shared MCode OAuth

新版 MiniMax Code 将登录态写入类似 `~/.minimax/auth/<buildEnv>/<region>/mcode-public/auth.json` 的文件。脚本会从 `records` 中选择有效期最晚的凭据，并用 Refresh Token 自助续期。

### 2. 与桌面端互斥

Refresh Token 是轮换制。脚本使用与桌面端兼容的目录锁，在锁内重新读取凭据、刷新、写回 `auth.json`，并同步 `auth-state.json` 的 generation，避免客户端与脚本同时刷新导致旧令牌作废。

### 3. 请求签名

签到接口需要时间戳、MD5 签名和固定时区参数。脚本按已验证的桌面端协议生成请求头与查询参数，并始终使用 `timezone_id=Asia/Shanghai`。

### 4. 幂等领取

脚本先查询 `/minimax-cloud/api/v1/signin/status`：

- 今日已经签到：直接返回 `ALREADY`，不重复领取。
- 今日可领取：`auto` 模式才调用 claim。
- `claim_result=1`：本轮领取成功。
- `claim_result=2`：服务端已领取过，按 `ALREADY` 处理。

### 5. 旧版兼容

如果找不到新版 OAuth 凭据，脚本可以扫描旧版 MiniMax leveldb，提取未过期的登录 JWT，并使用旧版请求头完成查询与领取。

---

## 🔑 准备认证文件

先在 MiniMax Code 桌面端完成登录，然后找到认证文件。默认路径形如：

```text
~/.minimax/auth/prod/cn/mcode-public/auth.json
```

不要把该文件提交到 Git，也不要发到 Issue、群聊或公开日志。文件结构只示意如下：

```json
{
  "schemaVersion": 1,
  "records": {
    "<record-key>": {
      "accessToken": "<ACCESS_TOKEN>",
      "refreshToken": "<REFRESH_TOKEN>",
      "expiresAtMs": 0,
      "generation": 1
    }
  }
}
```

脚本会优先自动查找默认路径。青龙、容器或 Actions 无法直接访问桌面目录时，用 `MINIMAX_OAUTH_AUTH_FILE` 指向实际文件。

---

## 🚀 部署方式一：青龙面板

| 步骤 | 操作 |
| :---: | :--- |
| **1. 上传脚本** | 将 `minimax_daily.py` 放到青龙脚本目录。 |
| **2. 准备凭据** | 将 `auth.json` 放到青龙可读的安全位置，并把绝对路径填入 `MINIMAX_OAUTH_AUTH_FILE`。 |
| **3. 新建任务** | 命令填 `task minimax_daily.py auto`，不要用裸 `python`。 |
| **4. 定时建议** | 每天一次，例如 `17 7 * * *`。青龙 cron 使用面板本地时间。 |

主流程没有第三方 Python 依赖。青龙中的认证文件必须可读写，因为 Refresh Token 轮换后脚本需要原子写回。

```bash
# 手动验证
task minimax_daily.py status
task minimax_daily.py auto
```

> 如果青龙容器无法访问桌面端认证文件，请先把 `auth.json` 安全地复制到容器持久目录，再设置 `MINIMAX_OAUTH_AUTH_FILE`。不要放在会被公开备份或日志采集的位置。

---

## ☁️ 部署方式二：GitHub Actions

工作流文件：[`.github/workflows/minimax.yml`](.github/workflows/minimax.yml)

- `push` 到 `main`：只运行测试、编译检查和 Ruff。
- `workflow_dispatch`：测试通过后，将 `MINIMAX_AUTH_JSON` 写入 `$RUNNER_TEMP/auth.json`，再运行 `python minimax_daily.py auto`。

### 添加 Secret

进入仓库 `Settings → Secrets and variables → Actions → New repository secret`：

| Secret | 必填 | 内容 |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | 手动运行时必填 | MiniMax `auth.json` 的完整 JSON 内容。不要加 Markdown 代码块。 |

### 运行

1. 打开仓库 `Actions` 页面。
2. 选择 `MiniMax Daily`。
3. 点击 `Run workflow`，选择 `main`。
4. 测试通过后，签到任务使用临时认证文件运行。

### 公开仓库不持久化轮换 Token

工作流只把认证文件写到当前 Runner 的 `RUNNER_TEMP`，**不会提交回仓库、不会上传为 Artifact，也不会在公开仓库持久化轮换后的 Refresh Token**。

这意味着：如果本轮触发 Refresh Token 轮换，Runner 结束后新令牌会随临时目录销毁。下一次运行仍使用 Secret 中的旧快照，可能得到 `invalid_grant`。需要长期无人值守时，应使用受控的私有运行环境安全保存更新后的 `auth.json`，并在每轮刷新后更新 Secret。v1.0.0 工作流刻意不自动提交凭据。

---

## 🔧 环境变量

| 变量 | 必填 | 默认 | 说明 |
| :--- | :---: | :--- | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | 条件必填 | 自动查找 | 新版 MiniMax OAuth `auth.json` 的路径。青龙、容器和 Actions 建议显式设置。 |
| `MINIMAX_LS_LEVELDB` | 可选 | 自动查找 | 旧版 MiniMax leveldb 目录覆盖路径。仅在新版 OAuth 凭据不存在时使用。 |
| `MINIMAX_DESKTOP_VERSION` | 可选 | `3.1.6` | 请求头中的 MiniMax 桌面端版本。仅在协议版本需要覆盖时设置。 |

环境变量只保存路径或版本，不应把 Token 原文写进命令历史、README 或日志。

---

## ⌨️ 命令行 CLI

```bash
python minimax_daily.py auto
python minimax_daily.py status
python minimax_daily.py login
```

| 命令 | 作用 | 是否写签到状态 |
| :--- | :--- | :---: |
| `auto` | 查询状态，今日可领时领取。默认命令。 | 是 |
| `status` | 只查询签到面板，不发送领取请求。 | 否 |
| `login` | 启动 Device Flow，在浏览器确认后写入新版 OAuth 凭据。 | 否 |

`login` 需要人工打开验证链接。青龙和 Actions 通常不具备交互条件，日常自动化应使用 `auto`。

---

## ✅ 成功判据

| 结果 | 含义 | 退出码 |
| :--- | :--- | :---: |
| `CLAIMED` | 本轮领取成功，服务端返回 `claim_result=1`。 | 0 |
| `ALREADY` | 今日已签，或领取接口返回幂等的 `claim_result=2`。 | 0 |
| `PENDING` | `status` 模式确认今日可领，但没有发送 claim。 | 0 |
| `INACTIVE` | 签到面板没有今日项，或今日不可领取。 | 0 |
| `NO_SESSION` | 登录态失效。 | 1 |
| `NETWORK` | 网络不可达。 | 1 |
| `NO_AUTH` | 没找到 OAuth 或旧版 JWT 凭据。 | 2 |
| `ERROR` | 接口、参数、JSON 或运行时异常。 | 1 或 2 |

只有服务端签到状态和领取回执可以判定成功。HTTP 200、空响应或只有脚本退出码都不能代替积分与状态回读。

输出示例：

```json
{"result":"ALREADY","report":"今日已签过（连签第 4 天）","day_no":4,"points":1000}
```

---

## 📁 目录结构

```text
MiniMax-Daily/
├── .github/workflows/minimax.yml
├── assets/
│   ├── donate-alipay.jpg
│   └── donate-wechat.png
├── docs/
│   ├── README.en.md
│   ├── README.zh-Hant.md
│   ├── README.ja.md
│   ├── README.ko.md
│   └── README.pt-BR.md
├── tests/test_minimax_daily.py
├── minimax_daily.py
├── requirements.txt
├── pyproject.toml
├── CHANGELOG.md
├── LICENSE
├── NOTICE.md
├── THIRD_PARTY_NOTICES.md
└── README.md
```

---

## 🧪 本地开发与验收

```bash
python -m unittest discover -s tests -p "test_minimax_daily.py" -v
python -m compileall -q minimax_daily.py tests
ruff check .
```

测试覆盖：

- 无凭据不误报成功。
- 今日已签不发送 claim。
- `status` 模式不产生写操作。
- 首次领取成功。
- 幂等 `claim_result=2` 按已签处理。
- 登录态失效可见。

---

## 🔒 隐私说明

- 仓库不包含账号、手机号、Access Token、Refresh Token、JWT 或设备信息。
- 脚本只输出状态、积分、连签天数等结果，不打印凭据原文。
- 认证文件由运行环境注入，`.gitignore` 已屏蔽 `auth.json`、`auth-state.json`、锁文件和运行日志。
- GitHub Actions 只在当前 Runner 的 `RUNNER_TEMP` 使用认证文件，不持久化到公开仓库。
- 提交 Issue 时请移除 Token、Cookie、账号标识、认证文件内容和完整网络抓包。

---

## ⚠️ 已知边界与免责声明

- MiniMax 可能调整 OAuth、签名或签到接口；接口变化时会返回 `INACTIVE`、`NO_SESSION` 或 `ERROR`，应以服务端回执为准。
- 活动未开启、账号无资格或服务端限制不属于脚本可绕过的本地问题。
- 本项目仅供学习与个人自动化使用。请遵守 MiniMax 服务条款，使用风险自负。
- 本项目是独立项目，与 MiniMax 官方无隶属、授权或背书关系。

---

## ☕ 支持与投喂

脚本完全免费，无广告，也没有功能门槛。如果它确实帮你节省了时间，欢迎自愿赞赏。赞赏不影响任何功能和 Issue 响应。

<p align="center">
  <img src="assets/donate-wechat.png" width="260" alt="微信赞赏码" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/donate-alipay.jpg" width="260" alt="支付宝收款码" />
</p>
<p align="center"><sub>💚 微信支付（左） &nbsp;|&nbsp; 💙 支付宝（右）</sub></p>

> 收款码仅用于向作者自愿赞赏。任何第三方以代下载、代部署、内部资源或会员群为由收费，均与作者无关。

---

## 💬 反馈与贡献

- 提交 [Issue](https://github.com/L0NE-6/MiniMax-Daily/issues) 报 Bug 或提出建议。
- 发起 [Pull Request](https://github.com/L0NE-6/MiniMax-Daily/pulls) 直接贡献代码。
- 提 Issue 时附上脱敏后的运行结果、复现步骤和 Python 版本。

---

## ✦ 星轨 Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star Trail" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>

---

<div align="center">
  <sub>L0NE-6 · DAILY SIGNAL &nbsp;|&nbsp; 点个 <b>Star</b>，让下一轮自动化有迹可循 ✨</sub>
</div>
