# 프로젝트 개요

## 대회 목표

- 대회명: 데이콘 스마트 창고 출고 지연 예측 AI 경진대회
- 목표: `avg_delay_minutes_next_30m` 예측
- 평가 지표: `MAE`

## 데이터 구조

- Train: `10,000` 시나리오 x `25` 슬롯 = `250,000`행
- Test: `2,000` 시나리오 x `25` 슬롯 = `50,000`행
- Layout
  - train layout: `250`
  - test layout: `100`
  - seen layout: `50`
  - test-only layout: `50`

## 문제 해석

이 문제는 단순 row-wise 회귀로 보기보다,
하나의 시나리오를 25개 슬롯으로 구성된 sequence로 보고 접근하는 것이 맞다고 판단하고 있습니다.

핵심 관점은 다음과 같습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `scenario scale`
   - 시나리오 내부 변동 크기
3. `slot deviation`
   - 각 슬롯이 baseline에서 얼마나 벗어나는지
4. `OOD / shift regime`
   - seen / unseen layout
   - 운영 상태 분포 이동
   - high-pressure / high-delay 구간

## EDA에서 얻은 핵심

### 1. baseline 비중이 크다

전체 variance 중 scenario baseline 비중이 크기 때문에,
row target을 직접 맞추는 것보다 baseline을 먼저 안정적으로 잡는 것이 중요합니다.

### 2. layout ID보다 운영 상태 shift가 더 중요하다

특히 중요한 축은 다음과 같습니다.

- `order_inflow_15m`
- `robot_active`
- `unique_sku_15m`
- `pack_pressure`
- `work_pressure`
- `pack_utilization`
- `low_battery_ratio`

즉, layout 그 자체보다 “운영 상태의 분포 이동”이 더 중요한 문제로 보고 있습니다.

### 3. deviation은 시간축과 압력 계열이 중요하다

슬롯 단위 편차에는 다음이 많이 작용합니다.

- `time_idx`
- `time_remaining`
- `pack_pressure`
- `robot_active`
- `order_inflow_15m`

## 모델 발전 흐름

### 1. 초기 ensemble

- LGBM
- Transformer
- LSTM
- STT
- TransLF

초기에는 강한 앙상블 베이스를 만드는 단계였습니다.

### 2. residual stack

- `a75 ~ a81`

강한 앵커 위에 residual correction을 얹는 구조로 public 점수를 천천히 낮췄습니다.

### 3. specialist 계열

- `a88`
- `a94`

representation residual, scenario baseline, shift/high/unseen specialist를 통합하면서 큰 점프를 만들었습니다.

### 4. decomposition + routing

- `a100`
- `a101`

최근에는 문제를

- baseline
- scale
- routed deviation

으로 다시 나누고,
`soft routing`으로 expert를 고르는 구조가 현재 메인 전략입니다.

## 현재 핵심 방향

현재는 `a94 family`를 더 정교하게 다듬는 것보다,
`a100 family`를 더 안정적이고 일관되게 만드는 것이 중요합니다.

현재 기준 메인 방향:

1. baseline / scale 안정화
2. z-space expert 유지
3. soft routing 유지
4. support/testlike는 보조 feature로 활용
5. hard subset mask보다 continuous correction 중심으로 접근

## 현재 최고 기록

- 파일: `submission_a101_10.csv`
- 점수: `10.1064209775`
- 날짜: `2026-04-21`
