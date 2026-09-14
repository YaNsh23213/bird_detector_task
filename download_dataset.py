import argparse
import re
from pathlib import Path

import gdown
import py7zr


def parse_args():
    parser = argparse.ArgumentParser(description="Download and extract dataset from Google Drive")
    parser.add_argument("--url", required=True, help="Google Drive share link to the archive")
    parser.add_argument("--dest", default="dataset", help="Destination folder for the extracted dataset")
    return parser.parse_args()


def extract_file_id(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        match = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError(f"Could not extract file id from URL: {url}")
    return match.group(1)


def main():
    args = parse_args()
    dest_dir = Path(args.dest)
    archive_path = Path("dataset.7z")
    file_id = extract_file_id(args.url)

    print(f"Downloading archive from Google Drive (id={file_id})...")
    gdown.download(id=file_id, output=str(archive_path), quiet=False)

    if not archive_path.exists():
        raise FileNotFoundError("Download failed: archive was not saved.")

    print(f"Extracting into {dest_dir}...")
    dest_dir.mkdir(parents=True, exist_ok=True)
    with py7zr.SevenZipFile(archive_path, mode="r") as archive:
        archive.extractall(path=dest_dir)

    archive_path.unlink()
    print(f"Done. Dataset extracted to: {dest_dir.resolve()}")


if __name__ == "__main__":
    main()