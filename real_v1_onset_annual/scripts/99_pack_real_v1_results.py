import argparse
from pathlib import Path
import zipfile
import yaml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    zip_path = outroot.with_suffix(".zip")
    include_ext = {".csv", ".json", ".yaml", ".yml", ".txt", ".md"}
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in outroot.rglob("*"):
            if p.is_file() and p.suffix.lower() in include_ext:
                z.write(p, p.relative_to(outroot))
    print(f"Wrote {zip_path}")

if __name__ == "__main__":
    main()
