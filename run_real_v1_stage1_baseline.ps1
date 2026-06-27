$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT
python -m real_v1_onset_annual.scripts.04_ews_dnb_baseline --config configs/real_v1_onset_annual.yaml
