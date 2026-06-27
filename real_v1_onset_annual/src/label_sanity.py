import pandas as pd


def summarize_labels(df: pd.DataFrame, horizon: int, node_col="node_id", year_col="year") -> dict:
    label = f"label_h{horizon}"
    valid = df[df["valid_eval"]].copy()
    return {
        "horizon": horizon,
        "n_rows_total": int(len(df)),
        "n_rows_valid": int(len(valid)),
        "n_nodes_total": int(df[node_col].nunique()),
        "n_nodes_valid": int(valid[node_col].nunique()),
        "n_years_valid": int(valid[year_col].nunique()),
        "positive_rows": int(valid[label].sum()) if label in valid.columns else 0,
        "positive_rate": float(valid[label].mean()) if len(valid) and label in valid.columns else None,
        "event_nodes": int(valid.loc[valid[label] == 1, node_col].nunique()) if label in valid.columns else 0,
        "min_year": int(valid[year_col].min()) if len(valid) else None,
        "max_year": int(valid[year_col].max()) if len(valid) else None,
    }


def add_status(summary: dict, pos_min=0.01, pos_max=0.15, warn=0.30) -> dict:
    pr = summary.get("positive_rate")
    status = "OK"
    notes = []
    if summary.get("n_nodes_valid", 0) == 186:
        status = "BAD"; notes.append("n_nodes_valid=186 indicates old restricted subset")
    if pr is None:
        status = "BAD"; notes.append("positive_rate is missing")
    else:
        if pr > warn:
            status = "BAD"; notes.append(f"positive_rate>{warn}; label likely too broad")
        elif pr < pos_min:
            status = "WARN"; notes.append(f"positive_rate<{pos_min}; positives may be too sparse")
        elif pr > pos_max:
            status = "WARN"; notes.append(f"positive_rate>{pos_max}; check label width")
    out = dict(summary)
    out["status"] = status
    out["notes"] = "; ".join(notes)
    return out
