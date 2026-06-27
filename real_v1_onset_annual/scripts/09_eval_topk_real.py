import argparse
from pathlib import Path
import yaml
import pandas as pd
from real_v1_onset_annual.src.topk_eval import eval_topk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    h = int(cfg["labels"]["primary_horizon"])
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "09_eval_topk_real"
    outdir.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(outroot / "02_onset_labels" / f"node_year_labeled_h{h}.csv")
    scores = pd.read_csv(outroot / "08_merged_scores" / "real_node_scores_by_year.csv")
    node_col = cfg["node"]["node_col"]
    year_col = cfg["node"]["year_col"]
    labels[node_col] = labels[node_col].astype(str)
    scores["node_id"] = scores["node_id"].astype(str)
    df = labels.merge(scores.rename(columns={"node_id": node_col}), on=[year_col, node_col], how="inner")
    df.to_csv(outdir / f"model_scores_with_labels_h{h}.csv", index=False, encoding="utf-8-sig")
    res = eval_topk(df, "node_score", f"label_h{h}", year_col=year_col, node_col=node_col, topk=cfg["evaluation"]["topk"], random_repeats=int(cfg["evaluation"]["random_repeats"]))
    res.to_csv(outdir / f"model_topk_eval_h{h}.csv", index=False, encoding="utf-8-sig")
    print(res.to_string(index=False))

if __name__ == "__main__":
    main()
