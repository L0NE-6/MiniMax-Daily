# Changelog

## v1.1.0 - 2026-11-24

- Added `MINIMAX_SITE=global` for the international MiniMax Code site
  (`agent.minimax.io` / `account.minimax.io`).
- Scoped OAuth credential discovery to the selected site region (`cn` or `en`).
- Added realUserID resolution from `MINIMAX_REAL_USER_ID`, desktop config, or
  the account identity API.
- Updated device-flow credential storage and state generation for the selected
  region.
- Added tests for site profiles and identity fallback.

## v1.0.0 - 2026-11-23

- Introduced the MiniMax Code sign-in implementation as an original L0NE-6
  project.
- Kept the original six sign-in tests and added the independent repository
  structure, Chinese and multilingual documentation, MIT licensing, third-party
  notices, donation assets, and GitHub Actions workflow.
- Added `MINIMAX_AUTH_JSON` handling for manual GitHub Actions runs. The secret
  is written only to `RUNNER_TEMP/auth.json`; public repositories do not persist
  rotated tokens.
