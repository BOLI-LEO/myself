import pandas as pd


def build_onset_table(event_df: pd.DataFrame, node_col="node_id", year_col="year", event_col="event") -> pd.DataFrame:
    df = event_df.copy()
    df[node_col] = df[node_col].astype(str)
    if "onset_year" in df.columns:
        out = df[[node_col, "onset_year"]].dropna().copy()
        out["onset_year"] = pd.to_numeric(out["onset_year"], errors="coerce")
        out = out.dropna(subset=["onset_year"])
        out["onset_year"] = out["onset_year"].astype(int)
        return out.drop_duplicates(node_col)
    if event_col not in df.columns:
        raise ValueError("Event table must contain onset_year or event column")
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    df[event_col] = pd.to_numeric(df[event_col], errors="coerce").fillna(0)
    pos = df[df[event_col] > 0].copy()
    onset = pos.groupby(node_col, as_index=False)[year_col].min()
    onset = onset.rename(columns={year_col: "onset_year"})
    onset["onset_year"] = onset["onset_year"].astype(int)
    return onset


def attach_onset_labels(node_year_df: pd.DataFrame, onset_df: pd.DataFrame, horizon: int, node_col="node_id", year_col="year") -> pd.DataFrame:
    df = node_year_df.copy()
    df[node_col] = df[node_col].astype(str)
    onset = onset_df.copy()
    onset[node_col] = onset[node_col].astype(str)
    df = df.merge(onset[[node_col, "onset_year"]], on=node_col, how="left")
    df["valid_eval"] = True
    has = df["onset_year"].notna()
    # Remove event year and post-event years.
    df.loc[has & (df[year_col] >= df["onset_year"]), "valid_eval"] = False
    # Positive if onset occurs in future h years.
    df[f"label_h{horizon}"] = (
        df["valid_eval"]
        & has
        & (df[year_col] < df["onset_year"])
        & (df["onset_year"] <= df[year_col] + horizon)
    ).astype(int)
    df["lead_to_onset"] = df["onset_year"] - df[year_col]
    return df
