#!/usr/bin/env python3
"""Version and release artifact naming for SocialMediaDownloadMaubot."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ARTIFACT_STEM = "SocialMediaDown-v"
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
MAUBOT_VERSION_RE = re.compile(r"^version:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
ARTIFACT_RE = re.compile(
    rf"^{re.escape(ARTIFACT_STEM)}(\d+)\.(\d+)\.(\d+)\.mbp$"
)


def version_tuple(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(version.strip())
    if not match:
        raise ValueError(f"Invalid version: {version!r}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def format_version(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"


def bump_version(major: int, minor: int, patch: int) -> tuple[int, int, int]:
    patch += 1
    if patch > 99:
        patch = 0
        minor += 1
    if minor > 99:
        minor = 0
        major += 1
    return major, minor, patch


def read_maubot_version(maubot_path: Path) -> str | None:
    text = maubot_path.read_text(encoding="utf-8")
    match = MAUBOT_VERSION_RE.search(text)
    return match.group(1) if match else None


def write_maubot_version(maubot_path: Path, version: str) -> None:
    text = maubot_path.read_text(encoding="utf-8")
    if not MAUBOT_VERSION_RE.search(text):
        raise ValueError(f"No version field in {maubot_path}")
    text = MAUBOT_VERSION_RE.sub(f"version: {version}", text, count=1)
    maubot_path.write_text(text, encoding="utf-8")


def versions_from_build_dir(build_dir: Path) -> list[tuple[int, int, int]]:
    if not build_dir.is_dir():
        return []
    found: list[tuple[int, int, int]] = []
    for path in build_dir.iterdir():
        match = ARTIFACT_RE.match(path.name)
        if match:
            found.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))
    return found


def max_version(*versions: tuple[int, int, int]) -> tuple[int, int, int] | None:
    return max(versions) if versions else None


def resolve_repo_paths(repo_dir: Path) -> tuple[Path, Path]:
    return repo_dir / "maubot.yaml", repo_dir / "build"


def current_version_tuple(repo_dir: Path) -> tuple[int, int, int]:
    maubot_path, build_dir = resolve_repo_paths(repo_dir)
    candidates: list[tuple[int, int, int]] = []

    maubot_version = read_maubot_version(maubot_path)
    if maubot_version:
        candidates.append(version_tuple(maubot_version))

    candidates.extend(versions_from_build_dir(build_dir))

    latest = max_version(*candidates)
    if latest is None:
        return 1, 0, 0
    return latest


def next_version_tuple(repo_dir: Path) -> tuple[int, int, int]:
    major, minor, patch = current_version_tuple(repo_dir)
    return bump_version(major, minor, patch)


def artifact_name(version: str) -> str:
    return f"{ARTIFACT_STEM}{version}.mbp"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("current", "peek", "bump", "artifact"),
        help="current: latest known; peek: next without write; bump: next and update maubot.yaml",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root",
    )
    parser.add_argument(
        "--version",
        help="Version for artifact command (default: current latest)",
    )
    args = parser.parse_args()

    repo_dir = args.repo.resolve()

    if args.command == "current":
        major, minor, patch = current_version_tuple(repo_dir)
        print(format_version(major, minor, patch))
        return 0

    if args.command == "peek":
        major, minor, patch = next_version_tuple(repo_dir)
        print(format_version(major, minor, patch))
        return 0

    if args.command == "bump":
        major, minor, patch = next_version_tuple(repo_dir)
        version = format_version(major, minor, patch)
        write_maubot_version(resolve_repo_paths(repo_dir)[0], version)
        print(version)
        return 0

    if args.command == "artifact":
        if args.version:
            version = args.version.strip()
            version_tuple(version)
        else:
            major, minor, patch = current_version_tuple(repo_dir)
            version = format_version(major, minor, patch)
        print(artifact_name(version))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
