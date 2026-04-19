# Experiment Log

## Best Public Score

- `10.1201425252`
- file: `submission_a88_27.csv`

## Major Milestones

- baseline: `11.83`
- `a48_v4_3`: `10.1477`
- `a56_3`: `10.1276`
- `a66_5`: `10.1260335184`
- `a75_01`: `10.122152212`
- `a76_01`: `10.121563682`
- `a77_01`: `10.1214405285`
- `a79_01`: `10.1214263184`
- `a81_01`: `10.121418246`
- `a83_01`: `10.1214032792`
- `a88_27`: `10.1201425252`

## What Changed In The Latest Phase

### a87

- major design change: TS2Vec-style representation branch
- direct prediction branch itself was not strong enough for direct submission
- important finding: the new representation signal was not best as a standalone predictor

### a88

- key change: reused the `a87` representation-driven signal as a residual feature instead of a final prediction
- strongest result came from applying the new signal only on layout-shift subsets
- this produced the best current score: `10.1201425252`

## Current Interpretation

- the recent bottleneck is not only low-band tuning anymore
- the better question is now: where should a new signal be applied
- `a88` suggests that representation-derived corrections are more useful on shift-heavy subsets than on the full test population

## Next Direction

- `a89`: shift-aware specialist refinement
- refine the shift mask using:
  - unseen layouts
  - large representation gap
  - high dispersion / weak flow layouts
  - layout-signal extremes
- goal: improve regime definition rather than only changing blend alpha
