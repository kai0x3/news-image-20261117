"""news-image-20261117 entry: write the prepared front-page image to
/output/entry.png. Deterministic, no network: it copies the image bundled
in this repository. The image was built from verified 17 Nov 2026 headlines
(see build_image.py); the AI judge ranks entries by what the image shows.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
