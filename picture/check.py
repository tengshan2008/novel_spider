from pathlib import Path

from . import db, gif
from .config import DB_FILE, IMAGES_PATH


def check_all():
    database = db.Database(DB_FILE)
    for item in database.read():
        page = gif.Page()

        dirpath = Path(IMAGES_PATH) / item["title"]
        filename = item["filename"]
        page.download_link(dirpath, item["url"], filename)

        filepath = dirpath / filename
        if filepath.exists():
            database.delete(item["url"])


if __name__ == "__main__":
    check_all()
