# 실험 로그

이 문서는 데이콘 스마트 창고 출고 지연 예측 대회에서 의미 있었던 실험 흐름을 요약합니다.

## 핵심 타임라인

| 날짜 | 단계 | public MAE | 의미 |
| --- | --- | ---: | --- |
| 2026-04-18 | 초기 ensemble/residual | `10.122152212` | low-band residual 보정으로 10.12대 진입 |
| 2026-04-20 | a94 | `10.1133848903` | scenario baseline + specialist 통합 |
| 2026-04-21 | a100 | `10.1090848449` | `baseline + scale + routed_z` 구조 확인 |
| 2026-04-22 | a101 | `10.1064209775` | soft expected-error router의 안정 구간 |
| 2026-04-26 | a114 | `10.103316418` | future-window pressure 피처가 의미 있음 |
| 2026-04-28 | a122 | `10.0967991272` | late/high-stress uplift로 10.09대 진입 |
| 2026-05-01 | a131 | `10.0920140626` | from-scratch direct signal microblend |
| 2026-05-02 | a137 | `10.02829` | raw-only reboot ensemble로 큰 점프 |
| 2026-05-02 | a138 | `10.0265043299` | raw-only fine grid |
| 2026-05-03 | a139 | `10.0208783095` | 공격적 tail expert |
| 2026-05-03 | a145_1755 | `10.0143960347` | future-pressure slot redistribution 성공 |
| 2026-05-03 | a145_4830 | `10.010757563` | 현재 최고 기록 |

## 실패에서 얻은 판단

- DANN/직접 domain-invariant 접근은 운영 상태 차이 안에 있는 예측 신호까지 지울 위험이 커서 주력 축에서 제외했습니다.
- support/testlike 신호는 feature로는 유용하지만 hard gating이나 hard fallback 기준으로 쓰면 public에서 크게 깨질 수 있었습니다.
- correction layer를 계속 얹는 방식은 local OOF에는 좋아 보여도 public에서 불안정했습니다.
- scenario-level bias correction은 residual 상관이 있더라도 최종 public 개선으로 바로 이어지지 않았습니다.

## 성공한 축

### 1. raw-only reboot

기존 제출 예측을 모델 입력으로 쓰지 않고 raw train/test/layout 기반 feature를 크게 확장하면서 `a137`, `a138`이 큰 점프를 만들었습니다.

주요 feature 방향은 다음과 같습니다.

- scenario aggregate
- future-window statistics
- warehouse pressure/load proxy
- slot rank/profile feature
- train/test 공통으로 계산 가능한 도메인 피처

### 2. future-pressure slot redistribution

2026-05-03의 가장 중요한 발견입니다.

단순히 scenario 평균을 올리거나 내리는 것이 아니라, 같은 scenario 안의 25개 슬롯에서 미래 압력이 큰 구간에 예측 질량을 더 배분했습니다. 이 구조가 `a145_1755`, `a145_4830`에서 public에 강하게 반응했습니다.

## 현재 다음 후보

| 후보 | 목적 | 판단 |
| --- | --- | --- |
| `submission_a149_008.csv` | `a145_4830`보다 더 공격적인 균형 후보 | 다음 1순위 제출 |
| `submission_a149_009.csv` | 더 강한 extrapolation | 9점대 도박 후보 |
| `submission_a149_085.csv` | 안정형 후보 | 안전하지만 돌파력은 약할 수 있음 |

## 현재 전략

이제 남은 간격은 작지만, `10.0107`에서 9점대로 들어가려면 단순한 0.001 개선이 아니라 public에서 한 번 더 맞는 공격적 후보가 필요합니다. 다음 실험은 `a145_4830`의 성공 모양을 기준으로, tail overshoot를 감시하면서 `a149` 계열을 제출하는 방향이 가장 유망합니다.
