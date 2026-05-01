# Resume / Portfolio Summary

## Project

DACON 스마트 창고 출고 지연 예측 AI 경진대회 참여  
향후 30분 평균 출고 지연 시간을 예측하는 MAE 최적화 문제를 해결했습니다.

## My Contributions

- 10,000개 train scenario와 2,000개 test scenario의 25-step 구조를 반영한 tabular-sequence modeling pipeline 설계
- layout generalization과 운영 상태 분포 이동을 고려한 scenario-level feature engineering
- CatBoost, LightGBM, Transformer, LSTM, residual ensemble 기반의 단계적 실험 수행
- `baseline + scale + routed_z` decomposition과 soft expected-error routing 구조 설계
- future-window, pressure, late-slot 관점의 피처 확장 및 public leaderboard 기반 검증
- late/high-stress underprediction 구간을 발견하고 public-safe uplift 전략으로 연속 개선
- from-scratch direct LGBM family를 새로 만들고, 기존 best anchor에 낮은 비율로 흡수하는 microblend 전략 검증
- OOF 성능과 public 성능이 어긋나는 후보를 prediction distribution 관점에서 필터링

## Technical Keywords

- Python
- CatBoost
- LightGBM
- GroupKFold
- Scenario-level Feature Engineering
- Time-series Tabular Modeling
- Residual Learning
- Mixture-of-Experts
- OOD Generalization
- Ensemble Optimization
- Experiment Tracking

## Outcome

- public leaderboard score를 `11.83` 기준선에서 `10.0920140626`까지 지속적으로 개선
- best public submission: `submission_a131_101.csv`
- 단순 모델 교체보다, 문제 구조를 baseline/scale/deviation, late/high-stress shift, direct model signal로 분해해 개선축을 검증
- 실패 실험도 기록해 aggressive correction, hard routing, 분포가 무너진 slot-direct 계열의 위험을 명확히 정리
