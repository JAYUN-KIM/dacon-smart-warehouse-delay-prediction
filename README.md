# DACON Smart Warehouse Delay Prediction

Personal competition portfolio for the DACON Smart Warehouse Delay Prediction challenge.

This repository tracks the full research path for predicting `avg_delay_minutes_next_30m`, including feature engineering, sequence modeling, residual learning, layout-aware experts, representation learning, and submission history.

## Project Summary

- Competition: DACON Smart Warehouse Delay Prediction
- Metric: MAE
- Goal: improve public/private generalization for 30-minute outbound delay prediction
- Current best public score: `10.1201425252`
- Current best file: `submission_a88_27.csv`

## What I Worked On

- layout-free feature engineering for operational signals
- Transformer, STT, LSTM, and LightGBM base model experiments
- residual CatBoost stack (`a75~a78`)
- sequence residual branches (`a79`, `a81`)
- layout-aware residual and layout-aware sequence residual (`a82`, `a83`)
- representation learning branch with TS2Vec-style direct signal (`a87`)
- representation-as-feature residual expert focused on layout shift (`a88`)

## Current Insight

The strongest recent signal is no longer pure low-band correction.

The important change from `a88` was:

- representation-driven residuals worked better on layout-shift subsets than on the full population
- this suggests the next meaningful improvement should come from better regime definition, not simply smaller alpha tuning
- the next planned direction is `a89`: shift-aware specialist refinement using representation gaps and layout-shift routing

## Repository Structure

- `docs/project_overview.md`
  high-level project direction and experiment evolution
- `docs/resume_summary.md`
  resume-friendly project summary
- `docs/experiment_log.md`
  milestone submissions and core findings
- `docs/daily_logs/`
  date-based progress notes
- `docs/public_score_log.json`
  public score history
- `scripts/update_daily_report.py`
  auto-generates daily summary files from the latest local experiment outputs

## Key Milestones

- `a75_01`: residual CatBoost jump to `10.122152212`
- `a79_01`: sequence residual branch to `10.1214263184`
- `a83_01`: layout-aware sequence residual to `10.1214032792`
- `a88_27`: representation-as-feature shift expert to `10.1201425252`

## Daily Workflow

1. run new experiments under `C:\open`
2. update score/history documents
3. run `python scripts/update_daily_report.py`
4. commit and push portfolio updates
