# Model logic: DNB-Reverse REAL-V1

## 1. Problem reformulation

Traditional early-warning models usually answer a graph-level question:

```text
Will the whole system transition?
```

This project answers a node-level question:

```text
Which nodes are likely to enter a precursor instability state before transition or degradation onset?
```

## 2. DNB-Reverse labeling

The core simulation-stage supervision is DNB-Reverse labeling.

Let \(\mathcal{D}(t^*)\) be the node set identified as DNB/CSD-consistent at future time \(t^*\). For an earlier window \(t\), node \(i\) is labeled positive if:

\[
y_i(t)=\mathbb{I}[\exists t^*\in(t,t+L], i\in\mathcal{D}(t^*)]
\]

This converts future mechanism-consistent DNB/CSD nodes into current learnable node labels.

## 3. Frozen model boundary

The frozen model should only do:

```text
standard graph-window tensor -> node precursor score
```

It should not do:

```text
Liu2019-specific parsing
mortality polygon parsing
real label construction
graph-level warning
old zero-shot validation
```

## 4. REAL-V1 real-data connection

Real data are transformed into annual node-year samples, onset labels, and 40-node graph patches. The frozen model is used as an inference backbone over these patches.

## 5. Evaluation

The real evaluation is TopK localization:

```text
Does TopK(score) enrich future onset/degradation nodes compared with random and EWS/DNB baselines?
```
