import argparse
from pathlib import Path
import yaml
from frozen_dnb_reverse.inference.merge_patch_scores import merge_scores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    ap.add_argument("--frozen_config", default="configs/frozen_model.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    fcfg = yaml.safe_load(open(args.frozen_config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "08_merged_scores"
    outdir.mkdir(parents=True, exist_ok=True)
    merge_scores(str(outroot / "07_patch_inference" / "patch_node_scores.csv"), str(outdir / "real_node_scores_by_year.csv"), mode=fcfg["inference"].get("aggregation_for_duplicate_nodes", "mean"))

if __name__ == "__main__":
    main()
