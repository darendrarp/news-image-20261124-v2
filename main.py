#!/usr/bin/env python3
"""Repo entrypoint TEMPLATE for a news-image edition (stdlib-only).

Copy this file into the edition repo as main.py, next to the rendered
entry.png, then set EXPECTED_SHA256 to the sha256 of entry.png:

    sha256sum entry.png

The renderer (draw.py, PIL) lives OUTSIDE the repo — the entrypoint only
copies the finished PNG to MAKEFUN_OUTPUT_DIR and verifies it, exactly
like our 20261124 entry (13 pass / 0 fail). Deterministic: two runs
write byte-identical output.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
# TODO: fill in after rendering — sha256sum entry.png
EXPECTED_SHA256 = "38c6c9ceb53918dff7c525b7856dd4e2a7080b4b50b3c15382e9c8c8eb5d9532"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {len(data)} bytes")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.png sha256 mismatch: {digest}")
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("entry.png is not a PNG file")
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if dest.read_bytes() != data:
        raise SystemExit("written copy differs from source")
    print(f"wrote {dest} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
