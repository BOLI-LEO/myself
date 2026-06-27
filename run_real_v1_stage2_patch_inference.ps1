$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT
python -m real_v1_onset_annual.scripts.05_build_real_graph --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.06_make_40node_patches --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.07_run_frozen_model_patch_inference --config configs/real_v1_onset_annual.yaml --frozen_config configs/frozen_model.yaml
python -m real_v1_onset_annual.scripts.08_merge_patch_scores --config configs/real_v1_onset_annual.yaml --frozen_config configs/frozen_model.yaml
