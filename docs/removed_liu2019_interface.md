# Removed Liu2019 / v257 interface

The previous v257 Liu2019 zero-shot interface is archived and not used as the main real-data validation layer.

## Reason

The legacy external validation had several problems:

1. It used a restricted node subset instead of full-node real data.
2. The label definition was too broad and produced excessive positive samples.
3. Onset-based relabeling showed that many selected nodes had already entered event state before the evaluation window.
4. It mixed model logic and real-data parsing logic.

## New rule

REAL-V1 uses a new real-data pipeline:

```text
full nodes -> annual samples -> onset labels -> EWS/DNB baselines -> 40-node patches -> frozen inference -> TopK evaluation
```
