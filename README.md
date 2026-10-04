. Batch Image Converter
markdown
# Batch Image Converter

Converts a folder of images to a different format in bulk, with optional resizing.

## Usage

python image_converter.py input_folder output_folder --format webp --quality 90 --recursive


## Options

| Flag | Description |
|------|-------------|
| `--format` | Target image format (e.g. jpg, png, webp) |
| `--quality` | Output quality for lossy formats, 1–100 (default: 85) |
| `--max_size` | Maximum width/height in pixels, preserves aspect ratio |
| `--recursive` | Also search subdirectories for images |

## Requirements

pip install Pillow
