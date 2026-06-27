import numpy as np
import pandas as pd
import networkx as nx


def build_graph_from_edges(edge_df: pd.DataFrame, src_col="src", dst_col="dst", weight_col="weight") -> nx.Graph:
    G = nx.Graph()
    for _, r in edge_df.iterrows():
        w = float(r[weight_col]) if weight_col in edge_df.columns else 1.0
        G.add_edge(str(r[src_col]), str(r[dst_col]), weight=w)
    return G


def build_knn_graph_from_xy(node_df: pd.DataFrame, node_col="node_id", x_col="x", y_col="y", k=4) -> nx.Graph:
    nodes = node_df[[node_col, x_col, y_col]].drop_duplicates(node_col).copy()
    nodes[node_col] = nodes[node_col].astype(str)
    xy = nodes[[x_col, y_col]].astype(float).values
    ids = nodes[node_col].values
    G = nx.Graph()
    G.add_nodes_from(ids)
    for i in range(len(ids)):
        d = np.sqrt(((xy - xy[i]) ** 2).sum(axis=1))
        order = np.argsort(d)
        for j in order[1:k+1]:
            G.add_edge(str(ids[i]), str(ids[j]), weight=float(np.exp(-d[j] / (np.median(d[order[1:k+1]]) + 1e-6))))
    return G


def adjacency_for_nodes(G: nx.Graph, node_ids: list[str]) -> np.ndarray:
    n = len(node_ids)
    idx = {v: i for i, v in enumerate(node_ids)}
    A = np.zeros((n, n), dtype=np.float32)
    for u, v, data in G.edges(data=True):
        if u in idx and v in idx:
            w = float(data.get("weight", 1.0))
            A[idx[u], idx[v]] = w
            A[idx[v], idx[u]] = w
    np.fill_diagonal(A, 1.0)
    return A
