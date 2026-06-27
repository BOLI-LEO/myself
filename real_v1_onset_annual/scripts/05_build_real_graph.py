import argparse
from pathlib import Path
import yaml
import pandas as pd
import networkx as nx
from real_v1_onset_annual.src.graph_builder import build_graph_from_edges, build_knn_graph_from_xy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "05_real_graph"
    outdir.mkdir(parents=True, exist_ok=True)
    edge_path = Path(cfg["paths"].get("edge_csv", ""))
    if edge_path.exists():
        edges = pd.read_csv(edge_path)
        G = build_graph_from_edges(edges)
    else:
        df = pd.read_csv(outroot / "01_node_year_dataset" / "node_year_features.csv")
        if "x" not in df.columns or "y" not in df.columns:
            raise ValueError("No edge_csv and no x/y columns for KNN graph")
        G = build_knn_graph_from_xy(df, node_col=cfg["node"]["node_col"], x_col="x", y_col="y", k=4)
    nx.write_gpickle(G, outdir / "real_graph.gpickle")
    pd.DataFrame([{"n_nodes": G.number_of_nodes(), "n_edges": G.number_of_edges()}]).to_csv(outdir / "real_graph_summary.csv", index=False)
    print(f"Graph nodes={G.number_of_nodes()} edges={G.number_of_edges()}")

if __name__ == "__main__":
    main()
