import argparse
import sys
from pathlib import Path
from PIL import Image


class ImageConverter:
    def __init__(self, input_dir, output_dir, target_format, quality=85, max_size=None, recursive=False):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_format = target_format
        self.quality = quality
        self.max_size = max_size
        self.recursive = recursive
        self.supported_formats = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"}

    def find_images(self):
        if self.recursive:
            return [p for p in self.input_dir.rglob("*") if p.suffix.lower() in self.supported_formats]
        return [p for p in self.input_dir.glob("*") if p.suffix.lower() in self.supported_formats]

    def convert_image(self, src_path, dst_path):
        pil_format = "JPEG" if self.target_format.lower() in ("jpg", "jpeg") else self.target_format.upper()
        with Image.open(src_path) as img:
            if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            if self.max_size:
                img.thumbnail((self.max_size, self.max_size))
            save_kwargs = {}
            if pil_format in ("JPEG", "WEBP"):
                save_kwargs["quality"] = self.quality
                save_kwargs["optimize"] = True
            img.save(dst_path, format=pil_format, **save_kwargs)

    def run(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        images = self.find_images()
        if not images:
            print("No images found to convert.")
            return
        for img_path in images:
            relative_path = img_path.relative_to(self.input_dir)
            dst_path = self.output_dir / relative_path.with_suffix(f".{self.target_format.lower()}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                self.convert_image(img_path, dst_path)
                print(f"Converted: {img_path} -> {dst_path}")
            except Exception as e:
                print(f"Failed to convert {img_path}: {e}", file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description="Convert images to a different format.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--format", type=str, required=True)
    parser.add_argument("--quality", type=int, default=85)
    parser.add_argument("--max_size", type=int, default=None)
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()
    if not args.input_dir.is_dir():
        print(f"Error: Input directory '{args.input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    return args


if __name__ == "__main__":
    args = parse_args()
    converter = ImageConverter(
        input_dir=args.input_dir, output_dir=args.output_dir, target_format=args.format,
        quality=args.quality, max_size=args.max_size, recursive=args.recursive,
    )
    converter.run()
