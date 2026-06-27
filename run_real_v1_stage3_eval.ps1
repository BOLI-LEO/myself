$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT
python -m real_v1_onset_annual.scripts.09_eval_topk_real --config configs/real_v1_onset_annual.yaml
python -m real_v1_onset_annual.scripts.99_pack_real_v1_results --config configs/real_v1_onset_annual.yaml
