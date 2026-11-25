#!/usr/bin/env python3
"""THE WORLD — Tuesday, 24 November 2026 (news-image-20261124 V2):
33 single-day stories, winner-formula V2.

Entrypoint for this news-image edition. The picture itself (entry.png)
was rendered beforehand; this script only places a verified copy of it
where the grader expects it. It reads entry.png from this repository,
copies it into the directory named by MAKEFUN_OUTPUT_DIR, and checks
that the copy's sha256 matches the hash recorded below.

The run is deterministic: running it twice writes byte-identical output.
Standard library only.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import NoReturn

# sha256 of entry.png in this repository (checked with `sha256sum entry.png`).
EXPECTED_SHA256 = "38c6c9ceb53918dff7c525b7856dd4e2a7080b4b50b3c15382e9c8c8eb5d9532"
# Largest image this entrypoint accepts (1 MiB).
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    source = repo_dir / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {output_dir}: {exc}")

    try:
        data = source.read_bytes()
    except OSError as exc:
        fail(f"cannot read {source}: {exc}")

    if len(data) > MAX_BYTES:
        fail(f"entry.png too large: {len(data)} bytes (limit {MAX_BYTES})")
    if not data.startswith(PNG_MAGIC):
        fail("entry.png is not a PNG file")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail(f"entry.png sha256 mismatch: got {digest}, expected {EXPECTED_SHA256}")

    dest = output_dir / "entry.png"
    shutil.copyfile(source, dest)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != EXPECTED_SHA256:
        fail("copied file does not match the expected sha256")
    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
