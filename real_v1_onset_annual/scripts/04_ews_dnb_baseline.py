import argparse
from pathlib import Path
import yaml
import pandas as pd
from real_v1_onset_annual.src.baseline_ews import add_baseline_scores
from real_v1_onset_annual.src.topk_eval import eval_topk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    h = int(cfg["labels"]["primary_horizon"])
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "04_ews_dnb_baseline"
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(outroot / "02_onset_labels" / f"node_year_labeled_h{h}.csv")
    df = add_baseline_scores(df)
    scored = outdir / f"baseline_scores_h{h}.csv"
    df.to_csv(scored, index=False, encoding="utf-8-sig")
    rows = []
    for col in ["score_ac1", "score_sd", "score_cv", "score_trend", "score_local_moran", "score_local_geary", "score_dnb_like"]:
        if col in df.columns:
            rows.append(eval_topk(df, col, f"label_h{h}", topk=cfg["evaluation"]["topk"], random_repeats=int(cfg["evaluation"]["random_repeats"])))
    res = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    res.to_csv(outdir / f"baseline_topk_eval_h{h}.csv", index=False, encoding="utf-8-sig")
    print(res.to_string(index=False))

if __name__ == "__main__":
    main()
