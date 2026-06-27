import numpy as np
import pandas as pd


def add_rolling_ews_features(df: pd.DataFrame, node_col: str, year_col: str, value_col: str = "ndvi", window: int = 5) -> pd.DataFrame:
    """Add simple annual EWS features per node.

    Features: ac1, sd, cv, trend. These are computed using previous `window` years including current year.
    """
    parts = []
    for node, g in df.groupby(node_col):
        g = g.sort_values(year_col).copy()
        vals = pd.to_numeric(g[value_col], errors="coerce")
        ac1, sd, cv, trend = [], [], [], []
        for idx in range(len(g)):
            s = vals.iloc[max(0, idx - window + 1): idx + 1].dropna().values
            if len(s) < 3:
                ac1.append(np.nan); sd.append(np.nan); cv.append(np.nan); trend.append(np.nan)
                continue
            sdv = float(np.std(s, ddof=1))
            meanv = float(np.mean(s))
            sd.append(sdv)
            cv.append(float(sdv / (abs(meanv) + 1e-6)))
            if len(s) >= 3 and np.std(s[:-1]) > 1e-8 and np.std(s[1:]) > 1e-8:
                ac1.append(float(np.corrcoef(s[:-1], s[1:])[0, 1]))
            else:
                ac1.append(np.nan)
            x = np.arange(len(s))
            trend.append(float(np.polyfit(x, s, 1)[0]))
        g["ac1"] = ac1
        g["sd"] = sd
        g["cv"] = cv
        g["trend"] = trend
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def fill_missing_feature_columns(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in feature_cols:
        if c not in out.columns:
            out[c] = 0.0
    for c in feature_cols:
        out[c] = pd.to_numeric(out[c], errors="coerce")
        out[c] = out[c].fillna(out[c].median() if out[c].notna().any() else 0.0)
    return out
