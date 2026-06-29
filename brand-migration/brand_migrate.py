#!/usr/bin/env python3
"""Scan and apply oneLib brand migration rules.

The script intentionally uses only the Python standard library so it can run
before project dependencies are installed.
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "brand-migration" / "config.yaml"
FINDINGS = ROOT / "brand-migration" / "findings.csv"


def token(*parts: str) -> str:
    return "".join(parts)


TEXT_REPLACEMENTS = {
    token("BIS", "HENG"): "ONELIB",
    token("Bi", "Sheng"): "oneLib",
    token("Bi", "sheng"): "oneLib",
    token("bi", "sheng"): "onelib",
    token("毕", "昇"): "一知",
    token("毕", "升"): "一知",
    token("data", "element", "/", "bi", "sheng"): "horacejett/oneLib",
    token("github.com/", "data", "element", "/", "bi", "sheng"): "github.com/horacejett/oneLib",
    token("https://github.com/", "data", "element", "/", "bi", "sheng"): "https://github.com/horacejett/oneLib",
    token("github.com/", "data", "element", "/", "onelib"): "github.com/horacejett/oneLib",
    token("https://github.com/", "data", "element", "/", "onelib"): "https://github.com/horacejett/oneLib",
    token("data", "element", "%2F", "onelib"): "horacejett%2FoneLib",
    token("data", "element", "/", "onelib"): "horacejett/onelib",
    token("data", "element", "/", "AgentGuidanceLanguage"): "horacejett/oneLib",
    token("data", "element", "/"): "horacejett/",
    token("Data", "element Technologies, Inc"): "oneLib",
    token("bi", "sheng", "-pyautogen"): "onelib-pyautogen",
    token("bi", "sheng", "_pyautogen"): "onelib_pyautogen",
    token("bi", "sheng", "-ragas"): "onelib-ragas",
    token("bi", "sheng", "_ragas"): "onelib_ragas",
    token("BIS", "HENG is an open LLM devops platform for next generation Enterprise AI applications."): "oneLib（一知）是面向企业知识库、智能体应用与生成式 AI 工作流的一体化平台。",
}

PATH_REPLACEMENTS = {
    token("BIS", "HENG"): "ONELIB",
    token("Bi", "Sheng"): "oneLib",
    token("Bi", "sheng"): "oneLib",
    token("bi", "sheng"): "onelib",
    token("毕", "昇"): "一知",
    token("毕", "升"): "一知",
}

NEEDLES = tuple(TEXT_REPLACEMENTS)
EXCLUDE_DIRS = {
    ".git",
    "brand-migration",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".venv",
    "__pycache__",
}
EXCLUDE_FILES = {
    "BRAND_MIGRATION_AUDIT.md",
}
TEXT_EXTS = {
    ".bat", ".cfg", ".conf", ".css", ".csv", ".dockerfile", ".env",
    ".go", ".html", ".ini", ".js", ".json", ".jsx", ".less", ".md",
    ".lock", ".mjs", ".mts", ".py", ".rst", ".scss", ".sh", ".sql", ".svg", ".toml",
    ".ts", ".tsx", ".txt", ".vue", ".xml", ".yaml", ".yml",
}
TEXT_NAMES = {
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "NOTICE",
    "README",
    ".gitignore",
    ".gitattributes",
}


def is_excluded(path: Path) -> bool:
    return path.name in EXCLUDE_FILES or any(part in EXCLUDE_DIRS for part in path.parts)


def is_text_candidate(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix.lower() in TEXT_EXTS


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and not is_excluded(path.relative_to(root)):
            yield path


def read_text(path: Path) -> str | None:
    if not is_text_candidate(path):
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None


def scan(root: Path) -> int:
    rows = []
    for path in iter_files(root):
        rel = path.relative_to(root)
        path_hits = [needle for needle in NEEDLES if needle in str(rel)]
        text = read_text(path)
        if text is None:
            if path_hits:
                rows.append([str(rel), "path", "|".join(path_hits), ""])
            continue
        for idx, line in enumerate(text.splitlines(), 1):
            hits = [needle for needle in NEEDLES if needle in line]
            if hits:
                rows.append([str(rel), idx, "|".join(hits), line[:500]])
        if path_hits:
            rows.append([str(rel), "path", "|".join(path_hits), ""])
    FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    with FINDINGS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "line", "hits", "sample"])
        writer.writerows(rows)
    print(f"findings: {len(rows)} -> {FINDINGS}")
    return len(rows)


def apply_text(root: Path) -> int:
    changed = 0
    for path in iter_files(root):
        text = read_text(path)
        if text is None:
            continue
        new_text = text
        for old, new in TEXT_REPLACEMENTS.items():
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"text files changed: {changed}")
    return changed


def rename_paths(root: Path) -> int:
    paths = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    changed = 0
    for path in paths:
        if path == root or is_excluded(path.relative_to(root)):
            continue
        new_name = path.name
        for old, new in PATH_REPLACEMENTS.items():
            new_name = new_name.replace(old, new)
        if new_name == path.name:
            continue
        target = path.with_name(new_name)
        if target.exists():
            raise FileExistsError(f"cannot rename {path} -> {target}: target exists")
        path.rename(target)
        changed += 1
    print(f"paths renamed: {changed}")
    return changed


def verify(root: Path) -> int:
    count = scan(root)
    if count:
        print("brand traces remain; inspect brand-migration/findings.csv")
    else:
        print("no configured brand traces remain")
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["scan", "apply-text", "rename-paths", "verify"])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    os.chdir(root)
    if args.command == "scan":
        return 0 if scan(root) >= 0 else 1
    if args.command == "apply-text":
        apply_text(root)
        return 0
    if args.command == "rename-paths":
        rename_paths(root)
        return 0
    if args.command == "verify":
        return 1 if verify(root) else 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
