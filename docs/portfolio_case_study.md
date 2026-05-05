# 포트폴리오 케이스 스터디

## 데이콘 스마트 창고 출고 지연 예측

### 한 줄 요약

스마트 창고의 시나리오별 25개 슬롯 운영 데이터를 바탕으로 향후 30분 평균 출고 지연 시간을 예측하는 문제에서, 단순 모델 고도화보다 **미래 압력 신호, 슬롯별 지연 재분배, 예측 분포 보정**이 더 중요하다는 것을 실험적으로 확인한 프로젝트입니다.

---

## 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 대회 | DACON 스마트 창고 출고 지연 예측 경진대회 |
| 문제 유형 | Tabular + time-series regression |
| 예측 대상 | `avg_delay_minutes_next_30m` |
| 평가 지표 | MAE |
| 데이터 구조 | train 10,000 scenarios x 25 slots, test 2,000 scenarios x 25 slots |
| 최종 public MAE | `10.0038814352` |
| 최종 제출 | `submission_a156_046.csv` |
| 개선폭 | 초기 기준 `11.83` → 최종 `10.0038814352`, 약 `1.8261` MAE 감소 |

---

## 내가 맡은 역할

- 전체 실험 파이프라인 설계 및 반복 개선
- scenario/slot 구조를 반영한 feature engineering
- CatBoost, LightGBM, sequence model, residual ensemble, MoE 구조 실험
- OOD/generalization 실패 분석 및 public leaderboard 기반 전략 수정
- 실험 로그, daily report, public score log, 최종 연구 요약 문서화
- 최종 포트폴리오/이력서용 실험 narrative 정리

---

## 문제를 어렵게 만든 핵심 조건

이 대회는 단순한 회귀 문제가 아니라, 운영 상태가 바뀌는 창고 환경에서 미래 지연을 예측해야 하는 문제였습니다.

### 1. Scenario 단위 독립성

각 scenario는 25개 슬롯으로 구성되어 있고, 같은 scenario 안의 슬롯 구조를 함께 봐야 했습니다. 단일 row를 독립적으로 예측하면 scenario 평균, 변동성, 슬롯 위치 정보를 충분히 활용하기 어려웠습니다.

### 2. 미래 30분 평균 지연 예측

타겟은 현재 지연이 아니라 `next_30m` 평균 지연이었습니다. 따라서 현재 슬롯의 값만 맞히는 것이 아니라, 앞선 1~2개 슬롯에서 나타나는 주문 유입, 로봇 가동, 병목 압력 신호가 이후 지연으로 어떻게 이어지는지를 반영해야 했습니다.

### 3. Public score와 local signal의 불일치

local OOF에서 좋아 보이는 correction, hard routing, pseudo-group 재가중이 public에서는 악화되는 경우가 많았습니다. 이 때문에 단순 평균 CV보다 예측 분포, tail shape, slot-wise redistribution을 함께 확인하는 방식으로 실험 기준을 바꿨습니다.

---

## 실험 흐름

### 1. 초기 ensemble과 residual model

초기에는 CatBoost, LightGBM, LSTM/Transformer 계열 sequence model, residual ensemble을 폭넓게 실험했습니다.

이 단계에서 public MAE를 `11.83` 수준에서 `10.12` 근처까지 낮췄지만, residual을 더 정밀하게 깎는 방식만으로는 10.1 근처에서 정체가 발생했습니다.

핵심 판단은 다음과 같았습니다.

- scenario baseline variance가 커서 row-level residual만 고도화하면 개선폭이 작다.
- 평균적으로 좋은 모델보다 특정 운영 regime에서 무너지는 오류를 줄여야 한다.
- public score는 local OOF보다 distribution shift와 tail shape에 더 민감했다.

### 2. Baseline + scale + routed deviation decomposition

중반에는 타겟을 직접 예측하는 대신 다음 구조로 분해했습니다.

```text
y = scenario_baseline + scenario_scale * routed_deviation
```

구성 요소는 다음과 같습니다.

- scenario-level baseline head
- robust scale head
- standardized deviation expert
- expected-error 기반 soft router
- global / shift-heavy / high-pressure / representation expert

이 접근은 `a100`, `a101` 계열에서 public `10.1064209775`까지 개선되며 구조적으로 유효하다는 것을 확인했습니다.

하지만 이후 correction layer를 더 얹는 방식은 local OOF에 과적합되는 경향이 강했습니다. 특히 hard routing, support-aware hard fallback, aggressive correction은 public에서 성능이 흔들렸습니다.

### 3. OOD routing 실패 분석

다음 접근들은 실험했지만 최종적으로 주력에서 제외했습니다.

- DANN/domain-invariant representation
- hard support-aware routing
- subset mask 기반 aggressive correction
- pseudo-group shift-heavy expert 재학습
- JTT 스타일 hard error reweighting

실패에서 얻은 판단은 명확했습니다.

- 도메인 차이를 지우면 예측 신호까지 지워질 수 있다.
- support/test-like score는 hard switch 기준이 아니라 보조 feature로 써야 한다.
- validation residual을 직접 correction target으로 삼으면 noise까지 학습할 위험이 크다.
- OOD 대응은 “불변 표현”보다 “조건부 specialization”에 가까웠다.

### 4. Future-window와 warehouse pressure feature

이후 문제를 다시 해석했습니다.

출고 지연은 현재 상태만의 결과가 아니라, 주문 유입, 로봇 가동률, SKU 다양성, 작업 압력, 포장 압력, layout 병목이 미래 몇 슬롯 뒤에 누적되어 나타나는 현상이라고 보았습니다.

추가한 feature 축은 다음과 같습니다.

- scenario aggregate statistics
- slot rank/profile feature
- future-window statistics
- order inflow / robot active / unique SKU pressure
- pack/work utilization
- path congestion proxy
- capacity gap proxy
- queue shock feature
- late/high-pressure uplift feature

이 방향은 `a114`, `a122`, `a127` 계열에서 꾸준한 개선을 만들었습니다.

### 5. Raw-only reboot

10.09 근처에서 미세 조정이 한계에 부딪히자, 기존 submission anchor를 보정하는 방식에서 벗어나 raw train/test/layout 기반으로 새 family를 만들었습니다.

대표 결과는 다음과 같습니다.

| 제출 | public MAE | 의미 |
| --- | ---: | --- |
| `submission_a137_011.csv` | `10.02829` | raw-only reboot ensemble로 큰 폭 개선 |
| `submission_a138_147.csv` | `10.0265043299` | raw-only fine grid |

이 전환은 포트폴리오 관점에서 중요한 장면입니다. 기존 best를 조금씩 깎는 방식이 아니라, 문제를 다시 정의하고 새로운 feature/model family를 만든 실험이었기 때문입니다.

### 6. Slot redistribution과 phase-lead

마지막 구간의 핵심은 scenario 평균을 크게 흔드는 것이 아니라, 같은 scenario 안에서 어느 슬롯에 지연을 더 배분할지 결정하는 것이었습니다.

최종적으로 효과가 있었던 관점은 다음과 같습니다.

- `next_30m` 타겟은 현재 슬롯보다 미래 1~2 슬롯의 압력 신호와 연결된다.
- future pressure가 높은 슬롯에 지연 예측을 재분배해야 한다.
- public-hit 후보의 p99/max tail shape를 기준으로 tail calibration을 해야 한다.
- 평균 예측보다 slot-wise distribution과 tail 보정이 중요하다.

대표 결과는 다음과 같습니다.

| 제출 | public MAE | 의미 |
| --- | ---: | --- |
| `submission_a145_1755.csv` | `10.0143960347` | future-pressure slot redistribution |
| `submission_a145_4830.csv` | `10.010757563` | scenario 평균 보존 + slot redistribution |
| `submission_a151_886.csv` | `10.0068002221` | queueing/domain reallocation |
| `submission_a155_481.csv` | `10.0046018208` | future phase-lead + tail 복원 |
| `submission_a156_046.csv` | `10.0038814352` | 최종 public-tail gamble |

---

## 주요 성과

### 정량적 성과

- 초기 public MAE `11.83`에서 최종 `10.0038814352`까지 개선
- 총 `1.8261` MAE 감소
- 10.12 정체 구간, 10.09 정체 구간, 10.02 정체 구간을 각각 다른 접근으로 돌파
- 최종적으로 9점대 진입에는 실패했지만, public 기준 10.00 초반까지 접근

### 정성적 성과

- 실험 실패와 성공을 날짜별로 문서화
- 모델 capacity보다 문제 정의와 예측 분포 설계가 중요하다는 근거 확보
- OOF와 public score가 불일치하는 상황에서 실험 의사결정 기준을 재설계
- 단순 모델링이 아니라 창고 운영/queueing 관점의 도메인 feature를 설계
- 최종적으로 이력서/포트폴리오에 설명 가능한 end-to-end 실험 흐름 확보

---

## 기술 스택

- Python
- pandas / NumPy
- LightGBM
- CatBoost
- residual learning
- sequence modeling
- Mixture-of-Experts
- scenario-level feature engineering
- OOD/generalization analysis
- prediction distribution calibration
- experiment tracking
- GitHub-based research logging

---

## 포트폴리오에서 강조할 수 있는 포인트

### 1. 단순 모델 성능 경쟁이 아니라 문제 재정의까지 수행

처음에는 모델 앙상블과 residual correction 중심으로 접근했지만, 최종적으로는 `next_30m` 예측이라는 문제 정의에 맞춰 future pressure와 phase-lead 구조를 설계했습니다.

### 2. 실패 실험을 버리지 않고 의사결정 근거로 활용

DANN, hard routing, aggressive correction, pseudo-group reweighting 등은 public에서 실패했지만, 이 실패를 통해 도메인 차이를 지우는 대신 조건부로 활용해야 한다는 방향성을 얻었습니다.

### 3. 작은 개선을 누적하다가도 필요하면 축을 갈아탐

10.09 근처에서 미세 조정의 한계를 확인한 뒤 raw-only reboot로 전환했고, 이 전환이 `10.0265`까지 큰 폭 개선을 만들었습니다.

### 4. 예측 분포와 tail calibration까지 관리

최종 구간에서는 평균 MAE만 보지 않고 p99/max tail, scenario 평균 보존, slot-wise redistribution을 함께 관리했습니다.

---

## 이력서용 압축 문장

아래 문장은 이력서나 포트폴리오 첫 화면에 그대로 사용할 수 있습니다.

> DACON 스마트 창고 출고 지연 예측 대회에서 10,000개 scenario x 25 slot의 tabular-time-series 데이터를 활용해 향후 30분 평균 출고 지연을 예측하는 파이프라인을 설계했습니다. CatBoost/LightGBM ensemble, baseline-scale-deviation decomposition, MoE routing, future-window pressure feature, queueing-inspired feature, slot redistribution 및 tail calibration을 단계적으로 실험하며 public MAE를 11.83에서 10.00388까지 개선했습니다.

---

## 면접에서 설명하기 좋은 질문

### Q. 가장 큰 성능 개선은 어디서 나왔나요?

초반에는 ensemble과 residual correction이 효과적이었지만, 가장 큰 전환은 raw-only reboot와 future-pressure slot redistribution이었습니다. 특히 target이 현재 지연이 아니라 향후 30분 평균 지연이라는 점을 다시 해석한 뒤, 미래 압력 신호를 현재 slot 예측에 phase-lead 형태로 반영한 것이 마지막 개선의 핵심이었습니다.

### Q. 왜 local validation이 아니라 public distribution을 많이 봤나요?

이 대회는 scenario/layout shift가 강했고, local OOF에서 좋아 보이는 hard correction이 public에서 악화되는 사례가 많았습니다. 그래서 단순 OOF MAE뿐 아니라 prediction distribution, tail shape, scenario 평균 보존 여부, slot-wise redistribution을 함께 검토했습니다.

### Q. 실패한 실험 중 가장 중요한 교훈은 무엇인가요?

DANN과 hard support-aware routing입니다. 도메인 차이를 제거하는 접근은 운영 상태 차이에 담긴 예측 신호까지 지울 수 있었고, hard routing은 경계 샘플에서 public 성능을 크게 흔들었습니다. 이 경험을 통해 OOD 문제를 불변 표현이 아니라 조건부 specialization과 soft calibration 문제로 해석하게 되었습니다.

---

## 최종 회고

이 프로젝트는 최종 목표였던 9점대에는 도달하지 못했습니다. 하지만 단순히 점수를 올리는 실험을 반복한 것이 아니라, 점수가 막힐 때마다 문제를 다시 정의하고, 실패한 방향을 문서화하고, 새로운 feature/model family를 설계해 끝까지 개선을 이어간 프로젝트였습니다.

포트폴리오에서는 “최종 순위”보다 다음 역량을 보여주는 사례로 활용할 수 있습니다.

- 불안정한 leaderboard 환경에서의 실험 설계
- OOD/generalization 실패 분석
- 문제 정의 기반 feature engineering
- prediction distribution calibration
- 실험 로그 기반 연구 문서화
- 끝까지 포기하지 않고 접근 방식을 바꾸는 실전형 문제 해결력
