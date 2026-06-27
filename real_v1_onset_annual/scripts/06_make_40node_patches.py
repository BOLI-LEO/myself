import argparse
from pathlib import Path
import yaml
import pandas as pd
import networkx as nx
from real_v1_onset_annual.src.patch_builder import build_patch_npz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "06_patches"
    outdir.mkdir(parents=True, exist_ok=True)
    G = nx.read_gpickle(outroot / "05_real_graph" / "real_graph.gpickle")
    h = int(cfg["labels"]["primary_horizon"])
    df = pd.read_csv(outroot / "02_onset_labels" / f"node_year_labeled_h{h}.csv")
    feature_cols = cfg["features"]["raw_features"] + cfg["features"]["ews_features"]
    years = sorted(df[cfg["node"]["year_col"]].unique().tolist())
    out_npz = outdir / "real_40node_patch_input.npz"
    build_patch_npz(df, G, feature_cols, years, str(out_npz), patch_size=int(cfg["graph"]["patch_size"]), window=int(cfg["features"]["window_length"]), max_patches=int(cfg["graph"]["max_patches_per_year"]), seed=int(cfg["graph"]["random_seed"]), node_col=cfg["node"]["node_col"], year_col=cfg["node"]["year_col"])
    print(f"Wrote {out_npz}")

if __name__ == "__main__":
    main()
