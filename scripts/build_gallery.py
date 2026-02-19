#!/usr/bin/env python3
"""
Build the photo gallery page from images in docs/images.

1. Converts any IMG_* HEIC files in docs/images to JPEG and removes the originals.
   (Uses Pillow + pillow-heif; install with: pip install -r requirements.txt)
2. Downsamples gallery images to max width 2000px (keeps aspect ratio).
3. Regenerates docs/gallery.html with all gallery images (jpeg/jpg/png, excluding logo).

Usage:
  pip install -r requirements.txt
  python scripts/build_gallery.py [--skip-convert]

  --skip-convert   Skip HEIC→JPEG conversion (e.g. if no HEICs).
"""

import argparse
import sys
from pathlib import Path

# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "docs" / "images"
GALLERY_HTML = REPO_ROOT / "docs" / "gallery.html"

# Gallery excludes (filenames that are not photos)
EXCLUDE = {"logo.png"}

# Max width for gallery images (downsampled in place)
MAX_WIDTH = 2000

# Image extensions to include in gallery (after any conversion)
GALLERY_EXTENSIONS = {".jpeg", ".jpg", ".png"}

# HEIC extensions to convert to JPEG
HEIC_EXTENSIONS = {".heic", ".HEIC"}


def convert_heic_to_jpeg(images_dir: Path) -> list[str]:
    """Convert IMG_* HEIC files to JPEG and delete originals. Returns list of new JPEG names."""
    try:
        from PIL import Image
        from pillow_heif import register_heif_opener
    except ImportError:
        print(
            "Error: HEIC conversion requires Pillow and pillow-heif. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    register_heif_opener()
    converted = []
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        if not path.name.startswith("IMG_"):
            continue
        if path.suffix not in HEIC_EXTENSIONS:
            continue
        jpeg_path = path.with_suffix(".jpeg")
        try:
            img = Image.open(path)
            # HEIC can be RGBA or other modes; JPEG needs RGB
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(jpeg_path, "JPEG", quality=92)
            path.unlink()
            converted.append(jpeg_path.name)
        except Exception as e:
            print(f"Warning: could not convert {path.name}: {e}", file=sys.stderr)
    return converted


def downsample_gallery_images(images_dir: Path) -> int:
    """Resize any gallery image wider than MAX_WIDTH to max width (aspect ratio preserved). Returns count resized."""
    try:
        from PIL import Image
    except ImportError:
        print(
            "Error: Downsampling requires Pillow. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    resized = 0
    for path in images_dir.iterdir():
        if not path.is_file() or path.name in EXCLUDE:
            continue
        if path.suffix.lower() not in {".jpeg", ".jpg", ".png"}:
            continue
        try:
            img = Image.open(path)
            if img.width <= MAX_WIDTH:
                continue
            ratio = MAX_WIDTH / img.width
            new_size = (MAX_WIDTH, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            # Save as JPEG for consistency and smaller size; PNG stays PNG if we want to preserve transparency
            save_kw = {"quality": 92} if path.suffix.lower() in (".jpeg", ".jpg") else {}
            img.save(path, "JPEG" if path.suffix.lower() in (".jpeg", ".jpg") else "PNG", **save_kw)
            resized += 1
        except Exception as e:
            print(f"Warning: could not downsample {path.name}: {e}", file=sys.stderr)
    return resized


def gallery_image_filenames(images_dir: Path) -> list[str]:
    """Return sorted list of image filenames to show in the gallery (excluding logo etc.)."""
    names = []
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        if path.name in EXCLUDE:
            continue
        if path.suffix.lower() in {".jpeg", ".jpg", ".png"}:
            names.append(path.name)
    return sorted(names)


def generate_gallery_html(image_filenames: list[str]) -> str:
    """Generate full gallery.html content with the given image filenames."""
    grid_items = []
    for name in image_filenames:
        # Friendly alt from filename (e.g. IMG_3818.jpeg -> Get Together Preschool photo)
        base = Path(name).stem
        alt = f"Get Together Preschool" if base.startswith("IMG_") else f"Get Together Preschool {base}"
        grid_items.append(
            f"""          <div class="rounded-xl overflow-hidden shadow-md hover:shadow-lg transition cursor-pointer">
            <img src="./images/{name}" alt="{alt}" class="w-full h-60 object-cover hover:scale-105 transition duration-300">
          </div>"""
        )
    grid_html = "\n".join(grid_items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Photo Gallery - Get Together Preschool</title>
  <meta name="description" content="Explore our preschool facilities, classrooms, and learning environments in San Jose.">
  <link rel="icon" href="./images/logo.png">
  <link rel="apple-touch-icon" href="./images/logo.png">
  <link rel="stylesheet" href="./css/site.css">
</head>
<body class="font-sans antialiased">
  <nav class="sticky top-0 z-50 bg-white shadow-sm border-b border-border">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
      <a href="./index.html" class="flex items-center gap-3 hover:opacity-80 transition">
        <img src="./images/logo.png" alt="Get Together Preschool" class="h-12 w-auto">
        <div>
          <h1 class="text-sm font-bold text-primary">Get Together San Jose Preschool</h1>
          <p class="text-sm text-muted-foreground font-kaiti">欢乐幼儿园</p>
        </div>
      </a>
      <div class="hidden md:flex gap-8 items-center">
        <a href="./index.html" class="text-sm font-medium text-foreground hover:text-primary transition">Home</a>
        <a href="./programs.html" class="text-sm font-medium text-foreground hover:text-primary transition">Programs</a>
        <a href="./gallery.html" class="text-sm font-medium text-primary transition">Gallery</a>
        <a href="./contact.html" class="text-sm font-medium text-foreground hover:text-primary transition">Contact</a>
        <a href="./apply.html" class="text-sm font-bold text-orange-500 hover:text-orange-600 transition">Apply</a>
      </div>
      <button id="mobile-menu-btn" class="md:hidden p-2 text-primary hover:bg-primary/10 rounded-lg transition" aria-label="Toggle menu">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden border-t border-border bg-white">
      <div class="px-4 py-2 flex flex-col gap-1">
        <a href="./index.html" class="text-sm font-medium text-foreground px-4 py-3 rounded-lg hover:bg-primary/10 hover:text-primary transition">Home</a>
        <a href="./programs.html" class="text-sm font-medium text-foreground px-4 py-3 rounded-lg hover:bg-primary/10 hover:text-primary transition">Programs</a>
        <a href="./gallery.html" class="text-sm font-medium text-primary px-4 py-3 rounded-lg hover:bg-primary/10 transition">Gallery</a>
        <a href="./contact.html" class="text-sm font-medium text-foreground px-4 py-3 rounded-lg hover:bg-primary/10 hover:text-primary transition">Contact</a>
        <a href="./apply.html" class="text-sm font-bold text-orange-500 px-4 py-3 rounded-lg hover:bg-orange-50 hover:text-orange-600 transition">Apply</a>
      </div>
    </div>
  </nav>

  <main class="min-h-screen bg-background">
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-yellow-50/30">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-primary mb-12 text-center">Gallery</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
{grid_html}
        </div>
      </div>
    </section>
  </main>

  <footer class="bg-primary text-primary-foreground py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-6">
        <p class="mb-4 font-semibold text-lg">Get Together Preschool | San Jose, California</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center text-sm">
          <a href="tel:+14089088105" class="hover:underline">(408) 908-8105</a>
          <span class="hidden sm:inline">|</span>
          <a href="mailto:get2getherpreschool@gmail.com" class="hover:underline">get2getherpreschool@gmail.com</a>
          <span class="hidden sm:inline">|</span>
          <a href="https://www.google.com/maps/search/?api=1&query=3394+Zisch+Dr+San+Jose+CA+95118" target="_blank" rel="noopener noreferrer" class="hover:underline">3394 Zisch Dr, San Jose, CA 95118</a>
        </div>
      </div>
      <p class="text-xs opacity-75 text-center mb-2">License #434417976</p>
      <p class="text-xs opacity-75 text-center">&copy; 2025 Get Together Preschool. All rights reserved.</p>
    </div>
  </footer>
  <script>
    // Mobile menu toggle
    (function() {{
      const mobileMenuBtn = document.getElementById('mobile-menu-btn');
      const mobileMenu = document.getElementById('mobile-menu');

      mobileMenuBtn.addEventListener('click', () => {{
        mobileMenu.classList.toggle('hidden');
      }});
    }})();
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert HEICs to JPEG and regenerate gallery.html")
    parser.add_argument(
        "--skip-convert",
        action="store_true",
        help="Skip HEIC to JPEG conversion (e.g. when not on macOS or no HEICs)",
    )
    args = parser.parse_args()

    if not IMAGES_DIR.is_dir():
        print(f"Error: images directory not found: {IMAGES_DIR}", file=sys.stderr)
        sys.exit(1)

    if not args.skip_convert:
        converted = convert_heic_to_jpeg(IMAGES_DIR)
        if converted:
            print(f"Converted {len(converted)} HEIC(s) to JPEG: {', '.join(converted)}")

    resized = downsample_gallery_images(IMAGES_DIR)
    if resized:
        print(f"Downsampled {resized} image(s) to max width {MAX_WIDTH}px.")

    names = gallery_image_filenames(IMAGES_DIR)
    if not names:
        print("Warning: no gallery images found in", IMAGES_DIR, file=sys.stderr)

    html = generate_gallery_html(names)
    GALLERY_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {GALLERY_HTML} with {len(names)} image(s).")


if __name__ == "__main__":
    main()
