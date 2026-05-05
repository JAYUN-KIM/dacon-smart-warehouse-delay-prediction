# 이력서 / 포트폴리오 요약

## 프로젝트

**DACON 스마트 창고 출고 지연 예측 경진대회**

스마트 창고의 scenario별 25개 slot 운영 데이터를 바탕으로 `avg_delay_minutes_next_30m`, 즉 향후 30분 평균 출고 지연 시간을 예측하는 MAE 회귀 문제를 수행했습니다.

## 핵심 성과

- 초기 public MAE `11.83`에서 최종 `10.0038814352`까지 개선
- 약 `1.8261` MAE 감소
- 최종 제출 파일: `submission_a156_046.csv`
- 10.12, 10.09, 10.02 정체 구간을 각각 다른 모델링/feature 축으로 돌파

## 주요 기여

- 10,000개 train scenario와 2,000개 test scenario의 25-slot 구조를 반영한 tabular-time-series modeling pipeline 설계
- CatBoost, LightGBM, sequence model, residual ensemble, Mixture-of-Experts 기반 실험 수행
- scenario baseline, scale, standardized deviation을 분리한 `baseline + scale * routed_z` decomposition 구조 설계
- expected-error 기반 soft routing과 specialist expert 구조 실험
- DANN, hard support-aware routing, aggressive correction 등 실패 실험을 분석하여 OOD 대응 전략 재설계
- future-window, warehouse pressure, queueing-inspired feature, slot redistribution, phase-lead feature 설계
- prediction distribution, p99/max tail, scenario 평균 보존 여부를 기준으로 public-safe calibration 수행
- 날짜별 실험 로그, public score log, 최종 연구 요약, 포트폴리오 문서 작성

## 기술 키워드

- Python
- pandas / NumPy
- LightGBM
- CatBoost
- Time-series tabular modeling
- Scenario-level feature engineering
- Residual learning
- Mixture-of-Experts
- OOD generalization
- Queueing-inspired feature engineering
- Prediction distribution calibration
- Experiment tracking

## 이력서용 Bullet

- DACON 스마트 창고 출고 지연 예측 대회에서 10,000개 scenario x 25 slot의 tabular-time-series 데이터를 활용해 향후 30분 평균 출고 지연 예측 파이프라인을 설계하고, public MAE를 `11.83`에서 `10.00388`까지 개선
- CatBoost/LightGBM ensemble, residual learning, `baseline + scale * routed_z` decomposition, MoE routing, future-window pressure feature, slot redistribution, tail calibration을 단계적으로 실험
- local OOF와 public leaderboard가 불일치하는 상황에서 hard routing과 aggressive correction의 실패 원인을 분석하고, 문제 정의 기반 feature engineering과 prediction distribution calibration 중심으로 전략 전환

## 포트폴리오용 소개 문단

이 프로젝트는 단순히 모델을 더 많이 쌓는 방식보다, 대회 문제 정의를 정확히 해석하는 것이 중요했던 사례입니다. 초반에는 ensemble과 residual correction으로 성능을 끌어올렸지만 10.1 근처에서 정체가 발생했습니다. 이후 `next_30m` 타겟의 의미를 다시 해석해 미래 주문 압력과 작업 병목이 어느 slot에서 지연으로 나타나는지를 feature와 예측 분포에 반영했고, raw-only reboot, queueing-inspired feature, future phase-lead, tail calibration을 통해 최종 public MAE `10.0038814352`까지 개선했습니다.
