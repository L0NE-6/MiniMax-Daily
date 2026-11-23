# 🧠 MiniMax Daily

**MiniMax Code 일일 출석 · OAuth 토큰 갱신 · 단일 파일 실행**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · **한국어** · [Português (BR)](README.pt-BR.md)

> **L0NE-6 오리지널 유지보수** · 버전: **v1.0.0** (2026-11-23)

## 사용 경계

공식 저장소와 Release 자산은 무료입니다. 유료 판매, 내부판 또는 독점판 재포장, 저작권 표시 제거, 작성자 이름과 후원 QR 코드를 이용한 공식 승인 사칭은 금지됩니다. 자세한 내용은 [NOTICE.md](../NOTICE.md)를 확인하세요.

## 기능

이 프로젝트는 MiniMax Code의 Shared MCode OAuth 인증 파일을 읽고, 액세스 토큰 만료가 가까우면 갱신한 뒤 오늘의 출석 상태를 조회합니다. 서버가 수령 가능하다고 응답한 경우에만 claim을 전송합니다. 구버전 클라이언트를 위한 leveldb JWT 경로도 유지합니다.

메인 흐름은 Python 표준 라이브러리만 사용하며 Python 3.8 이상을 지원합니다.

## 빠른 시작

1. MiniMax Code 데스크톱 클라이언트에서 로그인합니다.
2. 보통 `~/.minimax/auth/prod/cn/mcode-public/auth.json`에 있는 OAuth 파일을 찾습니다.
3. 다음 명령을 실행합니다.

```bash
python minimax_daily.py status
python minimax_daily.py auto
```

갱신된 인증 정보는 같은 파일에 원자적으로 기록됩니다. 실행 계정에 읽기와 쓰기 권한이 필요합니다.

## Qinglong

1. `minimax_daily.py`를 업로드합니다.
2. `auth.json`을 비공개 영구 디렉터리에 둡니다.
3. `MINIMAX_OAUTH_AUTH_FILE`을 해당 파일로 설정합니다.
4. 작업 명령을 `task minimax_daily.py auto`로 설정합니다.
5. 하루 한 번, 예를 들어 `17 7 * * *`이면 충분합니다.

## GitHub Actions

워크플로는 [`.github/workflows/minimax.yml`](../.github/workflows/minimax.yml)입니다.

- `main` push: 단위 테스트, 컴파일 검사, Ruff를 실행합니다.
- `workflow_dispatch`: `MINIMAX_AUTH_JSON`을 `$RUNNER_TEMP/auth.json`에 쓰고 `python minimax_daily.py auto`를 실행합니다.

| Secret | 필수 | 내용 |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | 수동 실행 시 필수 | MiniMax `auth.json`의 전체 JSON |

공개 저장소는 순환된 Token을 영구 저장하지 않습니다. 워크플로는 `auth.json`을 commit, upload 또는 저장하지 않으며 현재 Runner의 임시 디렉터리만 사용합니다. 실행 중 Refresh Token이 순환되면 작업 종료 후 새 값이 사라지므로 다음 실행 전에 Secret을 갱신해야 할 수 있습니다.

## 환경 변수

| 변수 | 필수 | 설명 |
| :--- | :---: | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | 조건부 | 새 OAuth `auth.json` 경로. |
| `MINIMAX_LS_LEVELDB` | 선택 | 구버전 leveldb 디렉터리 재정의. |
| `MINIMAX_DESKTOP_VERSION` | 선택 | 요청 헤더의 데스크톱 버전, 기본값 `3.1.6`. |

## CLI

| 명령 | 동작 |
| :--- | :--- |
| `python minimax_daily.py auto` | 상태를 확인하고 가능하면 출석합니다. |
| `python minimax_daily.py status` | 읽기 전용 상태 확인. |
| `python minimax_daily.py login` | Device Flow를 시작하고 브라우저 확인을 기다립니다. |

## 성공 기준

| 결과 | 의미 | 종료 코드 |
| :--- | :--- | :---: |
| `CLAIMED` | `claim_result=1`, 수령 성공. | 0 |
| `ALREADY` | 오늘 이미 수령했거나 멱등 응답 `claim_result=2`. | 0 |
| `PENDING` | 상태 확인에서 수령 가능하지만 claim은 보내지 않음. | 0 |
| `INACTIVE` | 오늘 활성 또는 수령 가능한 항목 없음. | 0 |
| `NO_SESSION` | 로그인 세션 무효. | 1 |
| `NETWORK` | 네트워크 요청 실패. | 1 |
| `NO_AUTH` | 인증 정보를 찾지 못함. | 2 |
| `ERROR` | API, JSON, 인자 또는 런타임 오류. | 1 또는 2 |

HTTP 200만으로 성공을 판단하지 않습니다. 서버 상태, claim 응답, 포인트와 연속 출석 일수를 확인해야 합니다.

## 개인정보와 면책

저장소에는 계정, 전화번호, Token, JWT 또는 기기 정보가 없습니다. 스크립트는 인증 값 원문을 출력하지 않습니다. Issue에 `auth.json`, Cookie 또는 인증된 전체 트래픽을 게시하지 마세요.

이 프로젝트는 MiniMax 공식과 제휴하거나 공식 승인을 받지 않았습니다. API는 변경될 수 있으며 서비스 약관을 준수하고 사용 위험은 사용자에게 있습니다.

## 후원

<p align="center">
  <img src="../assets/donate-wechat.png" width="220" alt="WeChat 후원 QR" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../assets/donate-alipay.jpg" width="220" alt="Alipay 후원 QR" />
</p>

QR 코드는 작성자에게 자발적으로 후원하기 위한 것입니다. 제3자가 다운로드, 대행 배포, 내부판 또는 회원 그룹 명목으로 비용을 요구하는 행위는 작성자와 무관합니다.

## Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>
