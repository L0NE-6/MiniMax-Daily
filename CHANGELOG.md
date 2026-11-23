# Changelog

## v1.0.0 - 2026-11-23

- Introduced the MiniMax Code sign-in implementation as an original L0NE-6
  project.
- Kept the original six sign-in tests and added the independent repository
  structure, Chinese and multilingual documentation, MIT licensing, third-party
  notices, donation assets, and GitHub Actions workflow.
- Added `MINIMAX_AUTH_JSON` handling for manual GitHub Actions runs. The secret
  is written only to `RUNNER_TEMP/auth.json`; public repositories do not persist
  rotated tokens.
