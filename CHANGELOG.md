# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `--version` flag; reads version from installed package metadata, falls back to `"0.1.0"`
- `warnings.warn()` when a multi-frame GIF or TIFF is passed — makes it explicit that only the first frame is used
- `Image.MAX_IMAGE_PIXELS` capped to Pillow's default (89,478,485 px) inside `combine_images()` and restored in `finally` — no global side-effect for library users

### Fixed
- `Image.open()` now uses a `with` statement; file handles are closed as soon as pixel data is loaded
- Skipped-file warnings in the CLI now go to `stderr` via `print()`, consistent with error output; removed `logging` module dependency
- Duplicate quality validation removed from `main()` — `ValueError` from `combine_images()` propagates to the existing error handler
- CI `ruff` now lints the entire repo (`ruff check .`) instead of only `image_combiner.py`
- Removed unused `_natural_sort_key` import from tests (was causing a hidden F401 lint failure)

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

[Unreleased]: https://github.com/csbisht/image-combiner/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/csbisht/image-combiner/releases/tag/v0.1.0
