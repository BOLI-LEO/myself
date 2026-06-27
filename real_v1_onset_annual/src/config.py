from pathlib import Path
import yaml


def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def ensure_dir(path: str | Path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
