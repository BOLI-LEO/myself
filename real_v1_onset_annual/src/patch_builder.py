import random
import numpy as np
import pandas as pd
import networkx as nx
from .graph_builder import adjacency_for_nodes


def bfs_patch(G: nx.Graph, start: str, size: int) -> list[str]:
    seen = []
    q = [start]
    visited = set([start])
    while q and len(seen) < size:
        u = q.pop(0)
        seen.append(u)
        for v in G.neighbors(u):
            if v not in visited:
                visited.add(v)
                q.append(v)
            if len(seen) + len(q) >= size:
                pass
    if len(seen) < size:
        # pad with existing nodes if graph component is small
        for v in G.nodes:
            if v not in visited:
                seen.append(v)
            if len(seen) >= size:
                break
    return seen[:size]


def make_patches(G: nx.Graph, patch_size=40, max_patches=500, seed=123) -> list[list[str]]:
    rng = random.Random(seed)
    nodes = list(map(str, G.nodes()))
    rng.shuffle(nodes)
    patches = []
    used_starts = nodes[:max_patches]
    for s in used_starts:
        p = bfs_patch(G, s, patch_size)
        if len(p) == patch_size:
            patches.append(p)
    # de-duplicate patches by node set
    uniq = []
    keys = set()
    for p in patches:
        key = tuple(sorted(p))
        if key not in keys:
            uniq.append(p); keys.add(key)
    return uniq


def build_patch_npz(node_year_df: pd.DataFrame, G: nx.Graph, feature_cols: list[str], years: list[int], out_npz: str, patch_size=40, window=5, max_patches=500, seed=123, node_col="node_id", year_col="year"):
    patches = make_patches(G, patch_size=patch_size, max_patches=max_patches, seed=seed)
    df = node_year_df.copy()
    df[node_col] = df[node_col].astype(str)
    Xs, As, node_ids_all, years_all, patch_ids = [], [], [], [], []
    for year in years:
        win_years = list(range(year - window + 1, year + 1))
        sub = df[df[year_col].isin(win_years)]
        for pid, nodes in enumerate(patches):
            arr = np.zeros((window, patch_size, len(feature_cols)), dtype=np.float32)
            ok = True
            for ti, yy in enumerate(win_years):
                gy = sub[sub[year_col] == yy].set_index(node_col)
                for ni, nid in enumerate(nodes):
                    if nid not in gy.index:
                        ok = False; break
                    vals = gy.loc[nid, feature_cols]
                    if hasattr(vals, "iloc") and len(getattr(vals, "shape", [])) > 1:
                        vals = vals.iloc[0]
                    arr[ti, ni, :] = vals.astype(float).values
                if not ok:
                    break
            if not ok:
                continue
            Xs.append(arr)
            As.append(adjacency_for_nodes(G, nodes))
            node_ids_all.append(nodes)
            years_all.append(year)
            patch_ids.append(f"y{year}_p{pid}")
    np.savez_compressed(out_npz, X=np.array(Xs), A=np.array(As), node_ids=np.array(node_ids_all, dtype=object), years=np.array(years_all), patch_ids=np.array(patch_ids, dtype=object), feature_cols=np.array(feature_cols, dtype=object))
    return out_npz
