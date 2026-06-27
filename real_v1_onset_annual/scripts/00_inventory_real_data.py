import argparse
from pathlib import Path
import pandas as pd
import yaml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outroot.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, path in cfg["paths"].items():
        if key.endswith("csv") or key.endswith("root"):
            p = Path(path)
            rows.append({"key": key, "path": str(p), "exists": p.exists(), "size_mb": p.stat().st_size/1024/1024 if p.exists() and p.is_file() else None})
    df = pd.DataFrame(rows)
    df.to_csv(outroot / "00_inventory.csv", index=False, encoding="utf-8-sig")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
