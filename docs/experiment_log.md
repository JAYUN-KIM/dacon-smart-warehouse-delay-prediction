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
| 2026-05-03 | a145_4830 | `10.010757563` | scenario 평균 보존형 slot redistribution |
| 2026-05-04 | a149_009 | `10.0073867868` | public-guided extrapolation |
| 2026-05-04 | a151_886 | `10.0068002221` | queueing/domain reallocation |
| 2026-05-04 | a155_481 | `10.0046018208` | future phase-lead + tail 복원 |
| 2026-05-04 | a156_046 | `10.0038814352` | 최종 public-tail gamble |

## 실패에서 얻은 판단

- DANN/직접 domain-invariant 접근은 운영 상태 차이 안에 있는 예측 신호까지 지울 위험이 커서 주력 축에서 제외했습니다.
- support/testlike 신호는 feature로는 유용하지만 hard gating이나 hard fallback 기준으로 쓰면 public에서 크게 깨질 수 있었습니다.
- correction layer를 계속 얹는 방식은 local OOF에는 좋아 보여도 public에서 불안정했습니다.
- scenario-level bias correction은 residual 상관이 있더라도 최종 public 개선으로 바로 이어지지 않았습니다.
- train target profile을 이용해 high-risk scenario의 시간 모양을 강제로 바꾸는 방식은 OOF/public 후보로 약했습니다.
- 마지막 구간에서 p99/max tail을 과하게 올리는 후보는 OOF가 좋아도 public에서 악화될 수 있었습니다.

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

### 3. future phase-lead

최종 제출 직전에는 문제 정의를 다시 확인했습니다. target은 현재 지연이 아니라 향후 30분 평균 지연이므로, 같은 scenario 안에서 앞으로 1~2 slot 뒤의 예측 및 운영 압력 신호를 현재 slot 예측에 반영하는 것이 자연스럽다고 판단했습니다.

이 방향으로 만든 `a154`는 local OOF를 크게 개선했지만, public에서 성공했던 p99/max tail이 낮아지는 문제가 있었습니다. 따라서 `a155`에서는 phase-lead를 유지하면서 tail shape를 다시 복원했고, `submission_a155_481.csv`가 public `10.0046018208`을 기록했습니다.

마지막 `a156`은 `a155_481`을 anchor로 두고 p99와 max만 한 단계 더 밀어 만든 최종 도박 후보입니다. `submission_a156_046.csv`가 public `10.0038814352`를 기록하며 대회를 마무리했습니다.

## 최종 전략 정리

최종적으로 가장 효과가 있었던 전략은 다음 순서였습니다.

1. raw-only reboot로 기존 anchor 의존을 끊고 feature space를 확장했습니다.
2. future-window/warehouse pressure feature로 미래 운영 상태를 예측에 반영했습니다.
3. scenario 평균을 크게 흔들기보다 25개 slot 안에서 예측 질량을 재분배했습니다.
4. 마지막에는 `next_30m` 정의에 맞춰 미래 1~2 slot 신호를 현재로 당기는 phase-lead를 적용했습니다.
5. public에서 민감했던 p99/max tail을 최종적으로 calibration했습니다.

목표였던 9점대에는 도달하지 못했지만, baseline `11.83`에서 최종 `10.0038814352`까지 꾸준히 개선했고, 실패한 방향과 성공한 방향을 모두 기록했습니다.
