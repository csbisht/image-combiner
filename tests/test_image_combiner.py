import pytest
from pathlib import Path
from PIL import Image

from image_combiner import combine_images
from image_combiner import _filter_and_sort


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_image(directory: Path, name: str, size=(100, 80), color=(255, 0, 0), mode="RGB") -> Path:
    """Create a solid-colour image and save it to *directory*."""
    path = directory / name
    Image.new(mode, size, color).save(path)
    return path


# ---------------------------------------------------------------------------
# combine_images — canvas size
# ---------------------------------------------------------------------------

class TestCanvasSize:
    def test_vertical_height_is_sum_of_inputs(self, tmp_path):
        a = make_image(tmp_path, "a.png", size=(100, 80))
        b = make_image(tmp_path, "b.png", size=(100, 60))
        out = tmp_path / "out.png"
        combine_images([a, b], out, direction="vertical")
        result = Image.open(out)
        assert result.size == (100, 140)  # height = 80 + 60

    def test_vertical_width_is_max_of_inputs(self, tmp_path):
        a = make_image(tmp_path, "a.png", size=(120, 50))
        b = make_image(tmp_path, "b.png", size=(80, 50))
        out = tmp_path / "out.png"
        combine_images([a, b], out, direction="vertical")
        assert Image.open(out).size[0] == 120  # width = max(120, 80)

    def test_horizontal_width_is_sum_of_inputs(self, tmp_path):
        a = make_image(tmp_path, "a.png", size=(100, 80))
        b = make_image(tmp_path, "b.png", size=(60, 80))
        out = tmp_path / "out.png"
        combine_images([a, b], out, direction="horizontal")
        assert Image.open(out).size == (160, 80)  # width = 100 + 60

    def test_horizontal_height_is_max_of_inputs(self, tmp_path):
        a = make_image(tmp_path, "a.png", size=(50, 120))
        b = make_image(tmp_path, "b.png", size=(50, 80))
        out = tmp_path / "out.png"
        combine_images([a, b], out, direction="horizontal")
        assert Image.open(out).size[1] == 120  # height = max(120, 80)


# ---------------------------------------------------------------------------
# combine_images — output formats
# ---------------------------------------------------------------------------

class TestOutputFormats:
    def test_jpeg_output_is_rgb(self, tmp_path):
        a = make_image(tmp_path, "a.jpg")
        b = make_image(tmp_path, "b.jpg")
        out = tmp_path / "out.jpg"
        combine_images([a, b], out)
        assert Image.open(out).mode == "RGB"

    def test_png_output_opens(self, tmp_path):
        a = make_image(tmp_path, "a.png")
        b = make_image(tmp_path, "b.png")
        out = tmp_path / "out.png"
        combine_images([a, b], out)
        assert Image.open(out) is not None

    def test_webp_output_opens(self, tmp_path):
        a = make_image(tmp_path, "a.png")
        b = make_image(tmp_path, "b.png")
        out = tmp_path / "out.webp"
        combine_images([a, b], out)
        assert Image.open(out) is not None

    def test_rgba_jpeg_has_white_background(self, tmp_path):
        # Fully transparent RGBA image — JPEG output should be white, not black.
        transparent = tmp_path / "t.png"
        Image.new("RGBA", (10, 10), (0, 0, 0, 0)).save(transparent)
        out = tmp_path / "out.jpg"
        combine_images([transparent], out)
        pixel = Image.open(out).convert("RGB").getpixel((5, 5))
        assert pixel == (255, 255, 255), f"Expected white background, got {pixel}"


# ---------------------------------------------------------------------------
# combine_images — DPI metadata
# ---------------------------------------------------------------------------

class TestDpi:
    def test_dpi_embedded_in_jpeg(self, tmp_path):
        a = make_image(tmp_path, "a.jpg")
        b = make_image(tmp_path, "b.jpg")
        out = tmp_path / "out.jpg"
        combine_images([a, b], out, dpi=300)
        info = Image.open(out).info
        assert info.get("dpi") == (300, 300)

    def test_dpi_embedded_in_png(self, tmp_path):
        a = make_image(tmp_path, "a.png")
        b = make_image(tmp_path, "b.png")
        out = tmp_path / "out.png"
        combine_images([a, b], out, dpi=150)
        # PNG stores DPI as dots-per-metre; Pillow converts back on read
        dpi = Image.open(out).info.get("dpi")
        assert dpi is not None
        assert round(dpi[0]) == 150


# ---------------------------------------------------------------------------
# combine_images — validation errors
# ---------------------------------------------------------------------------

class TestValidation:
    def test_invalid_direction_raises(self, tmp_path):
        a = make_image(tmp_path, "a.png")
        with pytest.raises(ValueError, match="direction"):
            combine_images([a], tmp_path / "out.png", direction="diagonal")

    def test_quality_too_low_raises(self, tmp_path):
        a = make_image(tmp_path, "a.jpg")
        with pytest.raises(ValueError, match="quality"):
            combine_images([a], tmp_path / "out.jpg", quality=0)

    def test_quality_too_high_raises(self, tmp_path):
        a = make_image(tmp_path, "a.jpg")
        with pytest.raises(ValueError, match="quality"):
            combine_images([a], tmp_path / "out.jpg", quality=96)

    def test_empty_list_raises(self, tmp_path):
        with pytest.raises(ValueError, match="No images"):
            combine_images([], tmp_path / "out.png")

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            combine_images([tmp_path / "ghost.jpg"], tmp_path / "out.jpg")


# ---------------------------------------------------------------------------
# _filter_and_sort — filtering and natural ordering
# ---------------------------------------------------------------------------

class TestFilterAndSort:
    def test_non_image_files_excluded(self, tmp_path):
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "photo.jpg:Zone.Identifier").touch()
        result = _filter_and_sort([
            str(tmp_path / "photo.jpg"),
            str(tmp_path / "notes.txt"),
            str(tmp_path / "photo.jpg:Zone.Identifier"),
        ])
        assert len(result) == 1
        assert result[0].name == "photo.jpg"

    def test_natural_sort_order(self, tmp_path):
        names = ["img_10.jpg", "img_2.jpg", "img_1.jpg"]
        for n in names:
            (tmp_path / n).touch()
        result = _filter_and_sort([str(tmp_path / n) for n in names])
        assert [p.name for p in result] == ["img_1.jpg", "img_2.jpg", "img_10.jpg"]

    def test_all_supported_extensions_accepted(self, tmp_path):
        extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp"]
        paths = []
        for ext in extensions:
            p = tmp_path / f"file{ext}"
            p.touch()
            paths.append(str(p))
        result = _filter_and_sort(paths)
        assert len(result) == len(extensions)
