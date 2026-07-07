from pathlib import Path
from zipfile import ZipFile

import nltk


BASE_DIR = Path(__file__).resolve().parent
NLTK_ROOT = Path("/root/nltk_data")

PACKAGES = [
    ("packages/tokenizers/punkt.zip", NLTK_ROOT / "tokenizers"),
    ("packages/tokenizers/punkt_tab.zip", NLTK_ROOT / "tokenizers"),
    ("packages/taggers/averaged_perceptron_tagger.zip", NLTK_ROOT / "taggers"),
    ("packages/taggers/averaged_perceptron_tagger_eng.zip", NLTK_ROOT / "taggers"),
]

RESOURCES = [
    "tokenizers/punkt",
    "tokenizers/punkt_tab",
    "taggers/averaged_perceptron_tagger",
    "taggers/averaged_perceptron_tagger_eng",
]


for relative_path, target_dir in PACKAGES:
    archive_path = BASE_DIR / relative_path
    if not archive_path.exists():
        raise FileNotFoundError(f"Missing NLTK vendor package: {archive_path}")

    target_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path) as archive:
        archive.extractall(target_dir)

for resource in RESOURCES:
    nltk.data.find(resource)
