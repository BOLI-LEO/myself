import argparse
from pathlib import Path
import pandas as pd


def merge_scores(patch_score_csv: str, out_csv: str, mode: str = "mean"):
    df = pd.read_csv(patch_score_csv)
    if mode == "mean":
        agg = df.groupby(["year", "node_id"], as_index=False)["node_score"].mean()
    elif mode == "max":
        agg = df.groupby(["year", "node_id"], as_index=False)["node_score"].max()
    elif mode == "median":
        agg = df.groupby(["year", "node_id"], as_index=False)["node_score"].median()
    else:
        raise ValueError("mode must be mean|max|median")
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patch_scores", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="mean", choices=["mean", "max", "median"])
    args = ap.parse_args()
    out = merge_scores(args.patch_scores, args.out, args.mode)
    print(f"Wrote {args.out}: rows={len(out)}")


if __name__ == "__main__":
    main()
