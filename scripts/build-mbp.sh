#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "$script_dir/.." && pwd)"
python_bin="${PYTHON:-python3}"

no_bump=0
output_path=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-bump)
            no_bump=1
            shift
            ;;
        *)
            output_path="$1"
            shift
            ;;
    esac
done

if [[ "$no_bump" -eq 1 ]]; then
    version="$("$python_bin" "$script_dir/release_version.py" current)"
else
    version="$("$python_bin" "$script_dir/release_version.py" bump)"
fi

if [[ -z "$output_path" ]]; then
    output_path="$repo_dir/build/SocialMediaDown-v${version}.mbp"
fi

if [[ "$output_path" != /* ]]; then
    output_path="$(pwd)/$output_path"
fi

build_dir="$(mktemp -d "${TMPDIR:-/tmp}/socialmediadownload-build.XXXXXX")"
payload_dir="$build_dir/payload"

cleanup() {
    find "$build_dir" -depth -delete
}
trap cleanup EXIT

mkdir "$payload_dir"

"$python_bin" -m pip install \
    --disable-pip-version-check \
    --no-compile \
    --no-deps \
    --requirement "$repo_dir/requirements.txt" \
    --target "$payload_dir"

if [[ -d "$payload_dir/bin" ]]; then
    find "$payload_dir/bin" -depth -delete
fi

cp "$repo_dir/base-config.yaml" "$payload_dir/"
cp "$repo_dir/maubot.yaml" "$payload_dir/"
cp "$repo_dir/socialmediadownload.py" "$payload_dir/"

"$python_bin" "$script_dir/package_mbp.py" "$payload_dir" "$build_dir/package.mbp"

mkdir -p "$(dirname "$output_path")"
mv -f "$build_dir/package.mbp" "$output_path"

"$python_bin" "$script_dir/verify-mbp.py" "$output_path"
echo "Built $output_path (version $version)"
