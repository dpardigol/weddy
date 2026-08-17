import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


ROOT = Path(__file__).parent

TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

CONFIG_FILE = ROOT / "site.json"
GALLERY_DIR = STATIC_DIR / "images" / "gallery"


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
}


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_gallery_images():

    if not GALLERY_DIR.exists():
        return []

    images = [
        image
        for image in GALLERY_DIR.iterdir()
        if image.is_file()
        and image.suffix.lower() in IMAGE_EXTENSIONS
    ]

    images.sort(key=lambda image: image.name.lower())

    return [
        f"images/gallery/{image.name}"
        for image in images
    ]


def prepare_dist():

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    DIST_DIR.mkdir(parents=True)


def copy_static():

    shutil.copytree(
        STATIC_DIR,
        DIST_DIR / "assets",
        dirs_exist_ok=True,
    )


def render_pages(config):

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
    )

    pages = [
        "index.html",
        "story.html",
        "details.html",
        "gallery.html",
    ]

    config["gallery"] = get_gallery_images()

    for page in pages:

        template = env.get_template(page)

        output = template.render(**config)

        destination = DIST_DIR / page

        destination.write_text(
            output,
            encoding="utf-8",
        )

        print(f"Generated {destination}")


def main():

    config = load_config()

    prepare_dist()
    copy_static()
    render_pages(config)

    print(
        f"\nWebsite generated successfully "
        f"with {len(config['gallery'])} gallery images."
    )


if __name__ == "__main__":
    main()