import argparse
from pathlib import Path
import yaml
from real_v1_onset_annual.src.data_io import read_csv_checked
from real_v1_onset_annual.src.onset_labels import build_onset_table, attach_onset_labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    in_csv = outroot / "01_node_year_dataset" / "node_year_features.csv"
    outdir = outroot / "02_onset_labels"
    outdir.mkdir(parents=True, exist_ok=True)
    node_col = cfg["node"]["node_col"]
    year_col = cfg["node"]["year_col"]
    node_year = read_csv_checked(in_csv)
    event = read_csv_checked(cfg["paths"]["event_csv"])
    onset = build_onset_table(event, node_col=node_col, year_col=year_col, event_col="event")
    onset.to_csv(outdir / "onset_table.csv", index=False, encoding="utf-8-sig")
    for h in cfg["time"]["horizons"]:
        labeled = attach_onset_labels(node_year, onset, int(h), node_col=node_col, year_col=year_col)
        # Keep only sample years.
        tcfg = cfg["time"]
        labeled = labeled[(labeled[year_col] >= int(tcfg["sample_start_year"])) & (labeled[year_col] <= int(tcfg["sample_end_year"]))].copy()
        out = outdir / f"node_year_labeled_h{h}.csv"
        labeled.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"Wrote {out}")

if __name__ == "__main__":
    main()
