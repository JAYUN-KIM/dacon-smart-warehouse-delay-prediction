# Experiment Log

## Best Public Score

- `10.1214032792`
- file: `submission_a83_01.csv`

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

## Notes

- `a75` was the first large jump from repeated blend tuning into residual modeling.
- `a79` introduced a sequence residual branch that improved public score.
- `a81` refined the sequence residual branch with a stronger hybrid sequence model.
- `a82` added a layout-aware residual expert using `layout_info.csv`.
- `a83` combined layout-aware signals and sequence residuals in one model and set the current best score.
