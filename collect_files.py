#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

src_path, dst_path, *extra = sys.argv[1:]
max_depth = int(extra[0]) if extra else -1

src, dst = map(lambda p: Path(p).resolve(), (src_path, dst_path))

def next_free_name(candidate: Path) -> Path:
    if not candidate.exists():
        return candidate
    stem, ext, idx = candidate.stem, candidate.suffix, 1
    while True:
        new = candidate.with_name(f"{stem}{idx}{ext}")
        if not new.exists():
            return new
        idx += 1

for item in src.rglob("*"):
    if item.is_file():
        rel_parts = item.relative_to(src).parts
        if max_depth > 0:
            rel_parts = rel_parts[-max_depth:]
        target_dir = dst.joinpath(*rel_parts[:-1])
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, next_free_name(target_dir / rel_parts[-1]))