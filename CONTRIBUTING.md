# Contributing to image-combiner

Thank you for taking the time to contribute! This document explains how to get the project running locally, how to submit changes, and what we expect from contributions.

---

## Getting started

### 1. Fork and clone

```bash
git clone https://github.com/csbisht/image-combiner.git
cd image-combiner
```

### 2. Set up the development environment

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

**Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements-dev.txt
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### 3. Verify everything works

```bash
python -m pytest tests/ -v
```

All tests should pass before you start making changes.

---

## Making changes

### Branch naming

Create a branch from `main` using one of these prefixes:

| Prefix | When to use |
|--------|-------------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation only |
| `chore/` | Maintenance, CI, dependencies |

```bash
git checkout -b feature/your-feature-name
```

### Code style

This project uses [ruff](https://docs.astral.sh/ruff/) for linting. Run it before committing:

```bash
ruff check image_combiner.py
```

Fix any reported issues before opening a pull request.

### Tests

- Add or update tests in `tests/test_image_combiner.py` for any change that affects behaviour.
- Use `tmp_path` (pytest built-in fixture) for temporary files — do not write to disk outside of it.
- All tests must pass:

```bash
python -m pytest tests/ -v
```

---

## Submitting a pull request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a pull request against the `main` branch.
3. Fill in the PR description — what changed and why.
4. CI will automatically run tests and lint checks. Both must pass before the PR can be merged.

---

## Reporting bugs

Open an issue at [github.com/csbisht/image-combiner/issues](https://github.com/csbisht/image-combiner/issues) and include:

- Your OS and Python version
- The exact command you ran
- The error message or unexpected output

---

## Questions

Open an issue with the `question` label and we will get back to you.
