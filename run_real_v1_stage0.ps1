$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT
python -m real_v1_onset_annual.scripts.00_inventory_real_data --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.01_build_node_year_dataset --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.02_build_onset_labels --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.03_label_sanity_check --config configs/real_v1_onset_annual.yaml
