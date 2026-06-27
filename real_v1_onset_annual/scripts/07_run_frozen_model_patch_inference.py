import argparse
from pathlib import Path
import yaml
from frozen_dnb_reverse.inference.patch_inference import run_inference


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/real_v1_onset_annual.yaml")
    ap.add_argument("--frozen_config", default="configs/frozen_model.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    fcfg = yaml.safe_load(open(args.frozen_config, "r", encoding="utf-8"))
    outroot = Path(cfg["paths"]["output_root"])
    outdir = outroot / "07_patch_inference"
    outdir.mkdir(parents=True, exist_ok=True)
    npz = outroot / "06_patches" / "real_40node_patch_input.npz"
    out_csv = outdir / "patch_node_scores.csv"
    run_inference(str(npz), str(out_csv), checkpoint_path=fcfg["model"].get("checkpoint_path"))

if __name__ == "__main__":
    main()
