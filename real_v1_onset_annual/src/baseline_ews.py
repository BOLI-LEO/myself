import numpy as np
import pandas as pd


def dnb_like_score(df: pd.DataFrame) -> pd.Series:
    sd = pd.to_numeric(df.get("sd", 0), errors="coerce").fillna(0)
    ac1 = pd.to_numeric(df.get("ac1", 0), errors="coerce").fillna(0)
    cv = pd.to_numeric(df.get("cv", 0), errors="coerce").fillna(0)
    # Simple DNB-like proxy for real-data baseline.
    raw = sd.rank(pct=True) + ac1.rank(pct=True) + cv.rank(pct=True)
    return raw / 3.0


def add_baseline_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in ["ac1", "sd", "cv", "trend", "local_moran", "local_geary"]:
        if c not in out.columns:
            out[c] = 0.0
        out[f"score_{c}"] = pd.to_numeric(out[c], errors="coerce").fillna(0).rank(pct=True)
    out["score_dnb_like"] = dnb_like_score(out)
    return out
