"""Combine multiple images into a single image, side-by-side or stacked."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image

__all__ = ["combine_images", "main"]

_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp"}


def _natural_sort_key(path: Path) -> list:
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", path.name)]


def _filter_and_sort(paths: list[str]) -> list[Path]:
    filtered = [Path(p) for p in paths if Path(p).suffix.lower() in _IMAGE_EXTENSIONS]
    return sorted(filtered, key=_natural_sort_key)


def combine_images(
    image_paths: Iterable[str | Path],
    output_path: str | Path,
    direction: str = "vertical",
    quality: int = 85,
    dpi: int | None = None,
) -> None:
    """Combine images horizontally or vertically into a single output image.

    Args:
        image_paths: Iterable of file paths to input images.
        output_path: File path for the saved output image.
        direction: 'vertical' (default) stacks images top-to-bottom;
                   'horizontal' places them left-to-right.
        quality: Output quality for JPEG/WebP, 1-95 (default 85).
        dpi: DPI value embedded in the output file metadata (e.g. 72, 150, 300).

    Raises:
        ValueError: If direction is not 'horizontal' or 'vertical'.
        ValueError: If quality is not in range 1-95.
        FileNotFoundError: If any input image path does not exist.
        OSError: If an image cannot be opened or the output cannot be saved.
    """
    if direction not in ("horizontal", "vertical"):
        raise ValueError("direction must be 'horizontal' or 'vertical'")
    if not (1 <= quality <= 95):
        raise ValueError("quality must be between 1 and 95")

    images: list[Image.Image] = []
    try:
        for path in image_paths:
            images.append(Image.open(path).convert("RGBA"))

        if not images:
            raise ValueError("No images provided")

        if direction == "horizontal":
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)
            canvas = Image.new("RGBA", (total_width, max_height))
            x = 0
            for img in images:
                canvas.paste(img, (x, 0), mask=img)
                x += img.width
        else:
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            canvas = Image.new("RGBA", (max_width, total_height))
            y = 0
            for img in images:
                canvas.paste(img, (0, y), mask=img)
                y += img.height

        save_kwargs: dict = {}
        if dpi is not None:
            save_kwargs["dpi"] = (dpi, dpi)

        save_path = Path(output_path)
        suffix = save_path.suffix.lower()
        if suffix in (".jpg", ".jpeg"):
            # Composite over white before dropping alpha; avoids black transparent areas
            background = Image.new("RGB", canvas.size, (255, 255, 255))
            background.paste(canvas, mask=canvas.getchannel("A"))
            background.save(output_path, quality=quality, **save_kwargs)
        elif suffix == ".webp":
            canvas.save(output_path, quality=quality, **save_kwargs)
        else:
            canvas.save(output_path, **save_kwargs)
    finally:
        for img in images:
            img.close()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Combine multiple images into one (vertical stack or side by side).\n"
            "Non-image files are skipped automatically. Numbered files are\n"
            "sorted in natural order (test_2 before test_10)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "supported formats:\n"
            "  jpg, jpeg, png, gif, bmp, tiff, tif, webp\n"
            "\n"
            "examples:\n"
            "  python3 image_combiner.py a.jpg b.jpg                          # vertical stack → combined.jpg\n"
            "  python3 image_combiner.py a.jpg b.jpg -o result.jpg            # save to result.jpg\n"
            "  python3 image_combiner.py a.jpg b.jpg -d horizontal            # side by side → combined.jpg\n"
            "  python3 image_combiner.py a.jpg b.jpg c.jpg -o out.png         # three images, PNG output\n"
            "  python3 image_combiner.py photos/*                             # all images in folder,\n"
            "                                                                  # auto-sorted and filtered\n"
            "  python3 image_combiner.py a.jpg b.jpg -q 95                   # high quality JPEG output\n"
            "  python3 image_combiner.py a.jpg b.jpg --dpi 300               # set 300 DPI (print quality)\n"
            "  python3 image_combiner.py a.jpg b.jpg -q 90 --dpi 150 -o out.jpg  # quality + DPI combined\n"
        ),
    )
    parser.add_argument(
        "images",
        nargs="+",
        metavar="IMAGE",
        help="Input image files (non-image files in the list are skipped)",
    )
    parser.add_argument(
        "-o", "--output",
        default="combined.jpg",
        help="Output file path (default: combined.jpg)",
    )
    parser.add_argument(
        "-d", "--direction",
        choices=["vertical", "horizontal"],
        default="vertical",
        help="Stack direction: vertical (default) or horizontal",
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=85,
        metavar="1-95",
        help="JPEG/WebP output quality 1-95 (default: 85, higher = better quality & larger file)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=None,
        metavar="DPI",
        help="Set output DPI metadata (e.g. 72=screen, 150=medium, 300=print; default: not set)",
    )
    return parser


def _print_brief_help(parser: argparse.ArgumentParser) -> None:
    print(parser.format_usage().rstrip())
    print("\nCombine multiple images into one (vertical stack or side by side).")
    print("Non-image files are skipped. Numbered files are sorted naturally.\n")
    print("positional arguments:")
    print("  IMAGE                 Input image files\n")
    print("optional arguments:")
    print("  -h, --help            show this help message and exit\n")
    print("Run with -h for full options, supported formats, and examples.")


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    if not (argv if argv is not None else sys.argv[1:]):
        _print_brief_help(parser)
        sys.exit(0)
    args = parser.parse_args(argv)
    if not (1 <= args.quality <= 95):
        print("Error: --quality must be between 1 and 95", file=sys.stderr)
        sys.exit(1)
    image_files = _filter_and_sort(args.images)
    skipped = set(args.images) - {str(p) for p in image_files}
    for s in sorted(skipped):
        print(f"Skipped (not an image): {s}", file=sys.stderr)
    try:
        combine_images(image_files, args.output, direction=args.direction,
                       quality=args.quality, dpi=args.dpi)
        print(f"Saved: {args.output}")
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
