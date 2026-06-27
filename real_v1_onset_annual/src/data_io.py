from pathlib import Path
import pandas as pd


def read_csv_checked(path: str, required: list[str] | None = None) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {p}")
    df = pd.read_csv(p)
    if required:
        miss = [c for c in required if c not in df.columns]
        if miss:
            raise ValueError(f"Missing columns in {p}: {miss}; existing={list(df.columns)}")
    return df


def normalize_node_year(df: pd.DataFrame, node_col="node_id", year_col="year") -> pd.DataFrame:
    out = df.copy()
    out[node_col] = out[node_col].astype(str)
    out[year_col] = pd.to_numeric(out[year_col], errors="coerce").astype("Int64")
    out = out.dropna(subset=[year_col])
    out[year_col] = out[year_col].astype(int)
    return out
