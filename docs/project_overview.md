# 프로젝트 개요

## 대회 목표

- 대회명: 데이콘 스마트 창고 출고 지연 예측 AI 경진대회
- 목표: `avg_delay_minutes_next_30m` 예측
- 평가 지표: `MAE`

## 데이터 구조

- Train: `10,000` 시나리오 x `25` 슬롯 = `250,000`행
- Test: `2,000` 시나리오 x `25` 슬롯 = `50,000`행
- 같은 시나리오 안의 25개 슬롯은 하나의 짧은 sequence처럼 해석 가능
- test에는 seen layout과 test-only layout이 함께 존재
- 핵심은 단순 row 회귀가 아니라 scenario-level 상태와 slot-level deviation을 동시에 맞히는 것

## 문제 해석

현재는 이 문제를 아래 5개 축으로 보고 있습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `scenario scale`
   - 시나리오 안에서 지연이 얼마나 흔들리는지
3. `slot deviation`
   - 각 슬롯이 baseline에서 얼마나 벗어나는지
4. `OOD / shift regime`
   - seen/test-only layout, 운영 상태 분포 이동, high-pressure/high-delay 구간
5. `future-window stress`
   - 같은 시나리오 내 25개 슬롯 전체에서 나타나는 가까운 미래 부하, 압력, 배터리 악화 신호

## 주요 피처 관점

중요하게 보고 있는 운영 변수는 다음과 같습니다.

- `order_inflow_15m`
- `robot_active`
- `unique_sku_15m`
- `pack_pressure`
- `work_pressure`
- `pack_utilization`
- `low_battery_ratio`
- `future_stress_score`
- `future_instability`
- `future_load_per_robot`

초기에는 단순 tabular/sequence ensemble이 중심이었지만, 점수가 줄어들수록 scenario baseline, scale, stress regime을 분리해서 보는 방식이 더 중요해졌습니다.

## 모델 발전 흐름

### 1. 초기 ensemble

초기에는 LGBM, Transformer, LSTM, STT, TransLF 계열을 섞어 강한 평균 예측기를 만들었습니다.

이 단계에서 `10.14`대에서 `10.12`대까지 내려왔습니다.

### 2. specialist 계열

`a88`, `a94`에서는 representation residual, scenario baseline, shift/high/unseen specialist를 결합했습니다.

성과:
- `a88_27 = 10.1201425252`
- `a94_51 = 10.1133848903`

이 단계에서 어려운 운영 구간을 따로 보는 specialist 방향이 유효하다는 점을 확인했습니다.

### 3. decomposition + routing

`a100`, `a101`에서는 문제를 다음처럼 분해했습니다.

```text
y_hat = baseline + scale * routed_z
```

구성:
- scenario baseline head
- scenario scale head
- standardized deviation expert
- soft expected-error router
- fallback

성과:
- `a100_05 = 10.1090848449`
- `a101_10 = 10.1064209775`

### 4. correction layer 실패 구간

`a102`, `a104`, `a105`, `a106`에서는 a101 앵커 위에 correction layer, hard subset, support-aware fallback 등을 얹었습니다.

결론:
- local OOF에서는 좋아 보이는 경우가 있었지만 public에서 흔들렸습니다.
- correction trigger, mask, magnitude가 local residual noise에 과적합될 수 있음을 확인했습니다.
- 이후에는 강한 correction layer를 우선순위에서 낮췄습니다.

### 5. future-window 해석

`a110` 이후에는 같은 시나리오 내 미래 슬롯 정보를 더 적극적으로 사용했습니다.

핵심 교훈:
- future-window 신호는 실제로 중요합니다.
- 하지만 row expert에 무작정 많이 넣는 것보다, scenario baseline/scale을 강화하는 방식이 더 안정적이었습니다.

성과:
- `a114_09 = 10.103316418`

### 6. clipped ridge delta

`a116`에서는 25개 슬롯을 한 번에 예측하는 ridge seq2seq direct family를 만들었습니다.

직접 모델 자체는 앵커보다 약했지만, 기존 앵커와 다른 방향의 delta를 제공했습니다. `a117`에서는 이 delta를 작게 clipping해서 앵커에 반영했습니다.

성과:
- `a117_09 = 10.1005923422`

이후 `a118`, `a119`에서 주변을 더 미세 조정했지만 public 개선은 실패했습니다. 따라서 clipped ridge delta family는 `a117_09` 근처에서 포화됐다고 판단했습니다.

### 7. high-error EDA와 late/high-stress uplift

`a121`에서는 `a117_09`가 크게 틀리는 시나리오를 다시 분석했습니다.

발견:
- high-error scenario는 랜덤 노이즈가 아니라 구조적 과소예측이었습니다.
- late slot에서 bias가 커졌습니다.
- `pack_pressure`, `pack_utilization`, `future_stress_score`가 높은 구간에서 오차가 크게 증가했습니다.

`a122`에서는 이 해석을 바탕으로 `a117_09` 앵커를 유지하고, stress risk가 높은 일부 구간에만 아주 작은 양수 uplift를 적용했습니다.

성과:
- `a122_1045 = 10.0967991272`

## 현재 최고 기록

- 파일: `submission_a122_1045.csv`
- 점수: `10.0967991272`
- 날짜: `2026-04-28`

## 현재 메인 방향

현재는 `a122_1045`를 새 앵커로 보고 있습니다.

다음 방향:

- `a122_1045`의 risk score 주변을 정밀 탐색
- `all_stress_small` 구성요소 조정
- shrink, bin, uplift cap을 public-safe 범위에서 탐색
- late/high-pressure/high-utilization 구간의 과소예측 보정 유지
- 평균 uplift와 max uplift가 과도해지지 않도록 제한

즉 지금은 새 모델을 크게 갈아엎는 단계가 아니라, public에서 검증된 오차 축을 더 정밀하게 파는 단계입니다.
