import argparse
from pathlib import Path
import yaml
import pandas as pd
from real_v1_onset_annual.src.data_io import read_csv_checked, normalize_node_year
from real_v1_onset_annual.src.annual_features import add_rolling_ews_features, fill_missing_feature_columns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"]) / "01_node_year_dataset"
    outroot.mkdir(parents=True, exist_ok=True)
    node_col = cfg["node"]["node_col"]
    year_col = cfg["node"]["year_col"]
    annual = read_csv_checked(cfg["paths"]["annual_feature_csv"], required=[node_col, year_col])
    annual = normalize_node_year(annual, node_col=node_col, year_col=year_col)
    tcfg = cfg["time"]
    annual = annual[(annual[year_col] >= int(tcfg["start_year"])) & (annual[year_col] <= int(tcfg["end_year"]))].copy()
    raw_features = cfg["features"]["raw_features"]
    annual = fill_missing_feature_columns(annual, raw_features)
    if "ndvi" in annual.columns:
        annual = add_rolling_ews_features(annual, node_col, year_col, value_col="ndvi", window=int(cfg["features"]["window_length"]))
    feature_cols = raw_features + cfg["features"]["ews_features"]
    annual = fill_missing_feature_columns(annual, feature_cols)
    out = outroot / "node_year_features.csv"
    annual.to_csv(out, index=False, encoding="utf-8-sig")
    meta = pd.DataFrame([{"n_rows": len(annual), "n_nodes": annual[node_col].nunique(), "min_year": annual[year_col].min(), "max_year": annual[year_col].max(), "feature_cols": ";".join(feature_cols)}])
    meta.to_csv(outroot / "node_year_features_summary.csv", index=False, encoding="utf-8-sig")
    print(f"Wrote {out}")
    print(meta.to_string(index=False))

if __name__ == "__main__":
    main()
