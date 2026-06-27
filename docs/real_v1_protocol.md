# REAL-V1-OnsetAnnual protocol

## Objective

Build a clean real-data experiment for annual remote-sensing precursor-node localization.

## Node unit

Use full forest grid nodes, preferably 1 km or 2 km grid cells. Avoid 30 m pixels as graph nodes.

## Time unit

Use annual growing-season composites. Do not use dense monthly samples as the first real experiment.

## Label

For node \(i\) with onset year \(T_i\), define:

\[
Y_i(t)=1 \quad \text{if} \quad t<T_i\le t+h
\]

Remove samples where \(t\ge T_i\).

## Sanity checks

A valid dataset should usually satisfy:

- full-node count, not 186-node subset
- positive rate around 1%–15%
- warning if positive rate > 30%
- enough negative stable samples
- no event-year leakage

## Main metrics

- TopK precision
- TopK hit rate
- Random precision
- Enrichment ratio
- Lead time
