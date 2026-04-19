# Project Overview

## Competition

- Title: DACON Smart Warehouse Delay Prediction
- Target: predict `avg_delay_minutes_next_30m`
- Metric: MAE

## Data Structure

- Train: 10,000 scenarios x 25 time slots = 250,000 rows
- Test: 2,000 scenarios x 25 time slots = 50,000 rows
- Layout split:
  - train layouts: 250
  - test layouts: 100
  - seen layouts: 50
  - train-only layouts: 200
  - test-only layouts: 50

## Research Evolution

The project evolved in distinct phases rather than one single model family.

### Phase 1: Strong tabular and sequence baselines

- `a18`: EDA threshold + LGBM baseline
- `a48`: Transformer + LSTM + LGBM ensemble
- `a56/a66`: STT + TransLF + a48 blend

### Phase 2: Residual stack

- `a75`: residual CatBoost was the first major jump
- `a76/a77/a78`: anchor-based residual refinement
- the main idea was to keep the strongest anchor and only learn the remaining error

### Phase 3: Sequence residual and layout-aware expansion

- `a79`: sequence residual branch
- `a81`: stronger sequence residual V2
- `a82`: layout-aware residual expert
- `a83`: layout-aware sequence residual

### Phase 4: Representation learning and shift-specific correction

- `a87`: TS2Vec-style representation branch
- `a88`: representation reused as a residual feature, not as a direct final predictor
- the best result from this phase came from applying the new signal only on layout-shift subsets

## Current View

The current project hypothesis is:

1. anchor-based residual learning is still the right backbone
2. pure low-band refinement is close to saturation
3. the new growth area is better regime definition
4. representation-derived signals appear to matter most on shift-heavy subsets

## Current Best Direction

The most promising next step is `a89`.

Planned idea:

- build a stronger shift-aware specialist
- define shift subsets using:
  - unseen layouts
  - representation gap to the anchor
  - layout compactness / dispersion / flow extremes
- apply the specialist only where the new signal is likely to help

This is currently the clearest path toward a larger jump than another round of low-band-only tuning.
