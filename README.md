# DNB-Reverse REAL-V1

A clean engineering package for a **frozen DNB-Reverse node-only precursor model** and a new **REAL-V1-OnsetAnnual** real-data validation pipeline.

This package deliberately separates:

1. `frozen_dnb_reverse/` — the frozen model interface. It accepts standardized graph-window tensors and outputs node precursor risk scores.
2. `real_v1_onset_annual/` — the new annual real-data experiment layer. It builds node-year samples, onset labels, real graph patches, baselines, and TopK evaluation.

The old Liu2019/v257 zero-shot interface is intentionally removed from the main workflow.

## Core logic

```text
Simulation-trained DNB-Reverse model
        ↓ freeze backbone
Standard graph-window input
        ↓
40-node real patches
        ↓
node precursor scores
        ↓
TopK evaluation against future onset labels
```

The real-data experiment is not graph-level warning. It is node-level precursor localization:

```text
Which nodes should be ranked as future precursor / degradation-onset candidates?
```

## Quick start

1. Edit `configs/real_v1_onset_annual.yaml` and set local data paths.
2. Run Stage 0 dataset construction and sanity checks:

```powershell
.\run_real_v1_stage0.ps1
```

3. Run baseline evaluation:

```powershell
.\run_real_v1_stage1_baseline.ps1
```

4. Build patches and run frozen-model inference:

```powershell
.\run_real_v1_stage2_patch_inference.ps1
```

5. Evaluate TopK:

```powershell
.\run_real_v1_stage3_eval.ps1
```

## Git policy

Commit code and configs only. Do **not** commit raw data, model checkpoints, `.csv`, `.npz`, `.pt`, `.zip`, or large outputs.

## Fixed model statement

The fixed precursor model should be documented as:

```text
DNB_Reverse_GNN node-only precursor model
Core source: v6n2.5.2 Cross-seed A
Complete frozen pipeline reference: v6n2.5.4 attribution full pipeline
Archived / not used: v257 Liu2019 zero-shot interface
```
