# Frozen DNB-Reverse model layer

This folder contains the interface for the frozen node-only DNB-Reverse precursor model.

The actual trained checkpoint should be stored outside Git, for example:

```text
D:/DNB_REAL_V1_LOCAL/checkpoints/frozen_dnb_reverse.pt
```

## Expected input `.npz`

```text
X:        [num_samples, window, 40, num_features]
A:        [num_samples, 40, 40]
node_ids: [num_samples, 40]
years:    [num_samples]
patch_ids:[num_samples]
```

## Expected output `.csv`

```text
year,patch_id,node_id,node_score
```

## Fallback mode

If the checkpoint is unavailable, `patch_inference.py` can output a heuristic score from the last feature channel or `dnb_like` feature. This is only for pipeline debugging, not final model evaluation.
