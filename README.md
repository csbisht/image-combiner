# image-combiner

A lightweight Python script to combine multiple images into a single file — stacked vertically or placed side by side.

---

## Why use this tool?

Sometimes you need to merge several images into one without opening a photo editor. This tool does exactly that from the command line — no GUI, no accounts, no subscriptions. It works on any machine that runs Python.

---

## What problems does it solve?

- You have 5 screenshots and want to share them as a single image
- You need to stitch a sequence of product photos into one file for a report or presentation
- You receive numbered files like `page_1.jpg`, `page_2.jpg`, ..., `page_10.jpg` and need them in the correct order (not `page_1`, `page_10`, `page_2`)
- Your folder has mixed files (`.jpg`, `.txt`, `.Zone.Identifier`) and you don't want to manually filter
- You want to automate image combining inside a script or pipeline using the Python API

---

## Where can it run?

| Platform | Supported |
|----------|-----------|
| Windows  | Yes       |
| macOS    | Yes       |
| Linux    | Yes       |

Runs anywhere Python 3.10+ is installed.

---

## Prerequisites

**Python 3.10 or higher** — works on Windows, macOS, and Linux (Ubuntu / Debian).

### Set up a virtual environment and install dependencies

A virtual environment keeps this project's dependencies isolated from your system Python.

**Windows**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **PowerShell note:** if you see a "running scripts is disabled" error, run this once and try again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**macOS / Linux (Ubuntu / Debian)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### What does `pip install -r requirements.txt` install?

| Package | Version | Purpose |
|---------|---------|---------|
| Pillow  | >=10.0.0 | Image reading, compositing, and saving across all supported formats |

### Verify the installation

```bash
python -c "from PIL import Image; print('Pillow OK')"
```

You should see:
```
Pillow OK
```

### Deactivate the virtual environment when you are done

```bash
deactivate
```

Your terminal prompt will return to normal, and the project's packages will no longer be active.

---

## Input & Output limits

| Item | Detail |
|------|--------|
| Minimum input images | 1 |
| Maximum input images | No hard limit (limited by available RAM) |
| Supported input formats | JPG, JPEG, PNG, GIF, BMP, TIFF, TIF, WebP (multi-frame GIF/TIFF: first frame only — a warning is printed) |
| Supported output formats | JPG, JPEG, PNG, GIF, BMP, TIFF, TIF, WebP |
| Quality range (JPEG/WebP) | 1 – 95 |
| DPI range | Any positive integer (common: 72, 150, 300) |
| Non-image files in input | Skipped automatically with a warning |

> Images are composited on a canvas sized to fit all inputs.
> For vertical stacks the canvas width = widest image.
> For horizontal layouts the canvas height = tallest image.
> Transparent areas are filled with white when saving as JPEG.

---

## Step-by-step guide for beginners

### 1. Clone the repository

```bash
git clone https://github.com/csbisht/image-combiner.git
```

### 2. Navigate to the project folder

```bash
cd image-combiner
```

### 3. Set up the virtual environment and activate it

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Common Windows errors

| Error | Cause | Fix |
|-------|-------|-----|
| `running scripts is disabled on this system` | PowerShell blocks unsigned scripts by default | Run once as Administrator: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `'python' is not recognized as an internal or external command` | Python is not installed or not added to PATH | Reinstall Python from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during setup |
| `'pip' is not recognized` | pip not on PATH or Python install is incomplete | Run `python -m pip install -r requirements.txt` instead of `pip install ...` |
| `'git' is not recognized` | Git is not installed | Download from [git-scm.com](https://git-scm.com/download/win) and restart the terminal after install |
| `venv\Scripts\activate.bat` does nothing | Wrong shell — `.bat` is for Command Prompt only | Use `venv\Scripts\Activate.ps1` in PowerShell instead |

### 4. Run your first combine

Stack two images on top of each other:

```bash
python image_combiner.py photo1.jpg photo2.jpg
```

This saves the result as `combined.jpg` in the current folder.

### 5. Choose a custom output name

```bash
python image_combiner.py photo1.jpg photo2.jpg -o result.png
```

### 6. Place images side by side

```bash
python image_combiner.py left.jpg right.jpg -d horizontal
```

### 7. Combine all images in a folder

```bash
python image_combiner.py photos/*
```

Files are sorted automatically in natural order (`img_2` before `img_10`). Non-image files are skipped.

---

## All command options at a glance

```
python image_combiner.py IMAGE [IMAGE ...] [options]
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output FILE` | `-o` | `combined.jpg` | Output file path and name |
| `--direction` | `-d` | `vertical` | `vertical` (top-to-bottom) or `horizontal` (left-to-right) |
| `--quality N` | `-q` | `85` | JPEG/WebP quality, 1–95. Higher = better quality, larger file |
| `--dpi N` | | not set | Embed DPI metadata (72 = screen, 150 = medium, 300 = print) |
| `--version` | | | Print version and exit |
| `--help` | `-h` | | Show full help with examples and exit |

Run with no arguments to see a quick usage summary:

```bash
python image_combiner.py
```

---

## Output examples

### Vertical stack (default)

```bash
python image_combiner.py top.jpg bottom.jpg -o stacked.jpg
```

```
top.jpg    ┌──────────┐
           │  image 1 │
           └──────────┘
bottom.jpg ┌──────────┐
           │  image 2 │
           └──────────┘
                 ↓
stacked.jpg ┌──────────┐
            │  image 1 │
            │  image 2 │
            └──────────┘
```

### Horizontal layout

```bash
python image_combiner.py left.jpg right.jpg -d horizontal -o side_by_side.jpg
```

```
left.jpg  right.jpg
┌───────┐ ┌───────┐
│  img1 │ │  img2 │     →    ┌───────┬───────┐
└───────┘ └───────┘          │ img1  │ img2  │
                             └───────┴───────┘
                             side_by_side.jpg
```

### High quality print export

```bash
python image_combiner.py scan1.png scan2.png -o print_ready.jpg -q 95 --dpi 300
```

Saves a 300 DPI JPEG at quality 95 — suitable for printing.

### Combine a whole folder

```bash
python image_combiner.py screenshots/* -o report.png
```

```
Skipped (not an image): screenshots/Thumbs.db
Saved: report.png
```

Non-image files are skipped with a message; everything else is combined in natural sort order.

---

## Using as a Python library

`combine_images` can be imported directly into your own scripts:

```python
from image_combiner import combine_images

combine_images(
    image_paths=["a.jpg", "b.jpg", "c.jpg"],
    output_path="result.jpg",
    direction="vertical",
    quality=90,
    dpi=150,
)
```

---

## ❤️ Sponsoring

If this tool saves you time, consider supporting its development:

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/csbisht)

---

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software.
The only requirement is that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.
