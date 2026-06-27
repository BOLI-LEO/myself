# Fixed model selection

## Selected model

The fixed precursor model is:

```text
DNB_Reverse_GNN node-only precursor localization model
```

## Source lineage

| Package | Role |
|---|---|
| `ef_pgnn_precursor_v6n2_5_2_crossseed_A` | Core DNB-Reverse model and cross-seed protocol |
| `ef_pgnn_precursor_v6n2_5_4_attribution_full_pipeline` | Complete frozen pipeline with post-hoc attribution |
| `v257_FIXED_ZERO_SHOT_shortpath` | Archived Liu2019 interface; not used in REAL-V1 |
| `DNB_REVERSE_GNN_V3_0_RUNNABLE` | Early runnable integration backup |

## What is frozen

- Node-only DNB-Reverse backbone
- Node risk scoring head
- Cross-seed learned precursor localization logic
- Optional post-hoc attribution tools

## What is removed

- Liu2019-specific interface
- v257 zero-shot scripts
- 186-node / mortality-only legacy validation
- graph-level warning branch as main task

## Engineering rule

The frozen model layer must not import files from the real-data adapter layer.
