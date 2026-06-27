import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def fallback_scores(X: np.ndarray) -> np.ndarray:
    """Return fallback node scores when no PyTorch checkpoint is available.

    X shape: [S, W, N, F]
    Uses the mean of last three feature channels at the final window step if available.
    This is a pipeline-debugging score, not the final frozen model.
    """
    last = X[:, -1, :, :]
    if last.shape[-1] >= 3:
        raw = np.nanmean(last[:, :, -3:], axis=-1)
    else:
        raw = np.nanmean(last, axis=-1)
    raw = np.nan_to_num(raw, nan=0.0)
    # standardize per sample
    mu = raw.mean(axis=1, keepdims=True)
    sd = raw.std(axis=1, keepdims=True) + 1e-6
    return sigmoid((raw - mu) / sd)


def run_inference(npz_path: str, out_csv: str, checkpoint_path: str | None = None):
    data = np.load(npz_path, allow_pickle=True)
    X = data["X"]
    node_ids = data["node_ids"]
    years = data["years"]
    patch_ids = data["patch_ids"]

    # Placeholder: final implementation should load the frozen DNB_Reverse_GNN checkpoint.
    # Current package provides a robust fallback to verify the REAL-V1 data pipeline.
    scores = fallback_scores(X)

    rows = []
    for s in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            rows.append({
                "year": int(years[s]),
                "patch_id": str(patch_ids[s]),
                "node_id": str(node_ids[s, j]),
                "node_score": float(scores[s, j]),
                "score_source": "fallback_debug_score" if not checkpoint_path else "frozen_checkpoint_placeholder",
            })
    out = pd.DataFrame(rows)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--checkpoint", default=None)
    args = ap.parse_args()
    out = run_inference(args.npz, args.out, args.checkpoint)
    print(f"Wrote {args.out}: rows={len(out)}")


if __name__ == "__main__":
    main()
