# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-29

### Added
- Core image combining functionality: vertical stack and side-by-side layouts
- RGBA → RGB conversion to ensure JPEG compatibility
- CLI entry point (`image-combiner`) via `pyproject.toml`; package is pip-installable
- Test harness with 18 tests covering core combining logic
- CI workflow running `pytest` and `ruff` on pull requests to `main`
- MIT License
- `CONTRIBUTING.md` with setup, branch, and PR guidelines
- `SECURITY.md` with vulnerability reporting policy
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1

[Unreleased]: https://github.com/csbisht/image-combiner/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/csbisht/image-combiner/releases/tag/v0.1.0
