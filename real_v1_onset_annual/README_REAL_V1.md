# REAL-V1-OnsetAnnual

A new clean real-data pipeline for annual onset-based precursor-node localization.

## Stages

0. Inventory raw real-data tables.
1. Build annual node-year dataset.
2. Build onset labels for h=1,2,3.
3. Run label sanity check.
4. Run EWS/DNB baselines.
5. Build real graph.
6. Make 40-node patches.
7. Run frozen model patch inference.
8. Merge duplicate patch scores.
9. Evaluate TopK against future onset labels.

## Required minimal annual feature table

Recommended columns:

```text
node_id, year, ndvi, ndmi, nbr, precip, temp, vpd, x, y
```

## Required minimal onset/event table

Option A:

```text
node_id, onset_year
```

Option B:

```text
node_id, year, event
```

The scripts will convert Option B into first onset year.
