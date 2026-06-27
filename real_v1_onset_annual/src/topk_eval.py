import numpy as np
import pandas as pd


def eval_topk(df: pd.DataFrame, score_col: str, label_col: str, year_col="year", node_col="node_id", topk=(3,5,10,20,50), random_repeats=500, seed=123) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    valid = df[df.get("valid_eval", True)].copy()
    rows = []
    for K in topk:
        prec, rand_prec, hit, recall = [], [], [], []
        for year, g in valid.groupby(year_col):
            if len(g) < K:
                continue
            g = g.sort_values(score_col, ascending=False)
            top = g.head(K)
            top_pos = int(top[label_col].sum())
            pos_total = int(g[label_col].sum())
            prec.append(top_pos / K)
            arr = g[label_col].values
            rp = []
            for _ in range(random_repeats):
                pick = rng.choice(len(arr), size=K, replace=False)
                rp.append(float(arr[pick].mean()))
            rand_prec.append(float(np.mean(rp)))
            if pos_total > 0:
                hit.append(1.0 if top_pos > 0 else 0.0)
                recall.append(top_pos / pos_total)
        m_prec = float(np.mean(prec)) if prec else np.nan
        m_rand = float(np.mean(rand_prec)) if rand_prec else np.nan
        rows.append({
            "score_col": score_col,
            "label_col": label_col,
            "K": K,
            "topk_precision": m_prec,
            "random_precision": m_rand,
            "enrichment": m_prec / (m_rand + 1e-12) if np.isfinite(m_prec) and np.isfinite(m_rand) else np.nan,
            "precision_gain": m_prec - m_rand if np.isfinite(m_prec) and np.isfinite(m_rand) else np.nan,
            "event_window_hit_rate": float(np.mean(hit)) if hit else np.nan,
            "event_window_recall": float(np.mean(recall)) if recall else np.nan,
            "n_years_eval": int(valid[year_col].nunique()),
        })
    return pd.DataFrame(rows)
