#!/usr/bin/env python3
"""Verify a built .mbp contains bundled deps and loads with maubot."""

from __future__ import annotations

import sys
import zipfile


def verify(path: str) -> None:
    required = (
        "maubot.yaml",
        "socialmediadownload.py",
        "instaloader/__init__.py",
    )
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = [name for name in required if name not in names]
        if missing:
            raise SystemExit(f"{path}: missing entries: {', '.join(missing)}")
        meta = archive.read("maubot.yaml").decode()
        if "instaloader" not in meta.split("modules:", 1)[-1]:
            raise SystemExit(f"{path}: instaloader not listed in maubot.yaml modules")

    try:
        from maubot.lib.zipimport import zipimporter
    except ImportError:
        print("verify-mbp: maubot not installed, skipped import check", file=sys.stderr)
        return

    importer = zipimporter(path)
    importer.load_module("instaloader")
    importer.load_module("socialmediadownload")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/plugin.mbp", file=sys.stderr)
        return 2
    verify(sys.argv[1])
    print(f"Verified {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
