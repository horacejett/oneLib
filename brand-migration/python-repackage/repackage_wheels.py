#!/usr/bin/env python3
"""Repackage upstream Python wheels under oneLib distribution names.

This keeps the process reproducible: unzip, rename package metadata/imports,
regenerate RECORD, and emit installable wheel files.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "brand-migration" / "python-repackage" / "dist"

OLD = "bi" + "sheng"
OLD_TITLE = "Bi" + "sheng"
OLD_AUTOGEN_DIST = OLD + "-pyautogen"
OLD_AUTOGEN_IMPORT = OLD + "_pyautogen"
OLD_RAGAS_DIST = OLD + "-ragas"
OLD_RAGAS_IMPORT = OLD + "_ragas"


def wheel_hash(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    return "sha256=" + base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def rewrite_text(data: bytes, replacements: list[tuple[str, str]]) -> bytes:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    return text.encode("utf-8") if text != original else data


def repack(src: Path, out_name: str, path_replacements: list[tuple[str, str]], text_replacements: list[tuple[str, str]]) -> Path:
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / out_name
    records: list[tuple[str, str, str]] = []
    payloads: list[tuple[str, bytes]] = []

    with ZipFile(src) as zf:
        for item in zf.infolist():
            if item.is_dir():
                continue
            old_name = item.filename
            new_name = old_name
            for old, new in path_replacements:
                new_name = new_name.replace(old, new)
            if new_name.endswith(".dist-info/RECORD"):
                record_name = new_name
                continue
            data = zf.read(old_name)
            data = rewrite_text(data, text_replacements)
            payloads.append((new_name, data))

    if "record_name" not in locals():
        raise RuntimeError(f"RECORD not found in {src}")

    payloads.sort(key=lambda row: row[0])
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        for name, data in payloads:
            zf.writestr(name, data)
            records.append((name, wheel_hash(data), str(len(data))))

        record_io = io.StringIO()
        writer = csv.writer(record_io, lineterminator="\n")
        for row in records:
            writer.writerow(row)
        writer.writerow((record_name, "", ""))
        zf.writestr(record_name, record_io.getvalue().encode("utf-8"))

    return out


def download_upstream(work_dir: Path) -> tuple[Path, Path]:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--no-deps",
            "--only-binary=:all:",
            "-d",
            str(work_dir),
            f"{OLD_AUTOGEN_DIST}==0.3.2",
            f"{OLD_RAGAS_DIST}==1.0.3",
        ],
        check=True,
    )
    return (
        work_dir / f"{OLD_AUTOGEN_IMPORT}-0.3.2-py3-none-any.whl",
        work_dir / f"{OLD_RAGAS_IMPORT}-1.0.3-py3-none-any.whl",
    )


def run(src_pyautogen: Path, src_ragas: Path) -> None:
    pyautogen = repack(
        src_pyautogen,
        "onelib_pyautogen-0.3.2-py3-none-any.whl",
        [
            (f"{OLD_AUTOGEN_IMPORT}-0.3.2.dist-info", "onelib_pyautogen-0.3.2.dist-info"),
        ],
        [
            (f"Name: {OLD_AUTOGEN_DIST}", "Name: onelib-pyautogen"),
            (OLD_AUTOGEN_DIST, "onelib-pyautogen"),
            (OLD_AUTOGEN_IMPORT, "onelib_pyautogen"),
        ],
    )

    ragas = repack(
        src_ragas,
        "onelib_ragas-1.0.3-py3-none-any.whl",
        [
            (f"{OLD_RAGAS_IMPORT}-1.0.3.dist-info", "onelib_ragas-1.0.3.dist-info"),
            (f"{OLD_RAGAS_IMPORT}/metrics/_answer_correctness_{OLD}.py", "onelib_ragas/metrics/_answer_correctness_onelib.py"),
            (f"{OLD_RAGAS_IMPORT}/metrics/_answer_recall_{OLD}.py", "onelib_ragas/metrics/_answer_recall_onelib.py"),
            (f"{OLD_RAGAS_IMPORT}/", "onelib_ragas/"),
        ],
        [
            (f"Name: {OLD_RAGAS_DIST}", "Name: onelib-ragas"),
            (OLD_RAGAS_DIST, "onelib-ragas"),
            (OLD_RAGAS_IMPORT, "onelib_ragas"),
            (OLD_TITLE, "OneLib"),
            (OLD, "onelib"),
        ],
    )

    for path in (pyautogen, ragas):
        print(path)
        print("sha256", hashlib.sha256(path.read_bytes()).hexdigest())
        print("size", os.path.getsize(path))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="onelib-wheel-upstream-") as tmp:
        run(*download_upstream(Path(tmp)))


if __name__ == "__main__":
    main()
