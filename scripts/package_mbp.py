#!/usr/bin/env python3
"""Create a maubot .mbp (zip) with POSIX path names inside the archive."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def package(payload_dir: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for file_path in sorted(payload_dir.rglob("*")):
            if not file_path.is_file():
                continue
            arcname = file_path.relative_to(payload_dir).as_posix()
            archive.write(file_path, arcname)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("payload_dir", type=Path)
    parser.add_argument("output_path", type=Path)
    args = parser.parse_args()
    package(args.payload_dir.resolve(), args.output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
