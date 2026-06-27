import argparse
from pathlib import Path
import yaml
import pandas as pd
from real_v1_onset_annual.src.label_sanity import summarize_labels, add_status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "03_label_sanity"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for h in cfg["time"]["horizons"]:
        f = outroot / "02_onset_labels" / f"node_year_labeled_h{h}.csv"
        df = pd.read_csv(f)
        s = summarize_labels(df, int(h), node_col=cfg["node"]["node_col"], year_col=cfg["node"]["year_col"])
        s = add_status(s, pos_min=float(cfg["labels"]["positive_rate_min"]), pos_max=float(cfg["labels"]["positive_rate_max"]), warn=float(cfg["labels"]["positive_rate_warn"]))
        rows.append(s)
    out = pd.DataFrame(rows)
    out.to_csv(outdir / "label_sanity_summary.csv", index=False, encoding="utf-8-sig")
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
