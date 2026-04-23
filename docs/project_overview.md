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

이 문제는 단순한 row-wise 회귀보다는, 하나의 시나리오를 25개 슬롯으로 구성된 sequence로 보고 해석하는 쪽이 더 잘 맞았습니다.

현재는 문제를 아래 4개 층으로 나눠서 보고 있습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `scenario scale`
   - 시나리오 내부 변동성의 크기
3. `slot deviation`
   - 각 슬롯이 baseline에서 얼마나 벗어나는지
4. `OOD / shift regime`
   - seen / unseen layout
   - 운영 상태 분포 이동
   - high-pressure / high-delay 구간

## EDA에서 얻은 핵심 인사이트

### 1. baseline 비중이 크다

전체 variance 중 scenario baseline 비중이 커서, row target을 직접 맞추는 것보다 baseline을 먼저 안정적으로 맞추는 것이 중요하다고 판단했습니다.

### 2. layout ID보다 운영 상태 shift가 더 중요하다

특히 아래 변수들이 중요했습니다.

- `order_inflow_15m`
- `robot_active`
- `unique_sku_15m`
- `pack_pressure`
- `work_pressure`
- `pack_utilization`
- `low_battery_ratio`

즉 layout ID 자체보다, 운영 상태의 분포 이동이 더 큰 문제라는 해석을 유지하고 있습니다.

### 3. slot deviation은 시간축과 압력 계열이 중요하다

슬롯 단위 편차는 아래 변수가 많이 좌우했습니다.

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

초기에는 강한 동상블 베이스를 만드는 단계였습니다.

### 2. residual stack

- `a75 ~ a81`

강한 앵커 위에 residual correction을 얹는 구조로 public 점수를 조금씩 내렸습니다.

### 3. specialist 계열

- `a88`
- `a94`

representation residual, scenario baseline, shift/high/unseen specialist를 통합하면서 큰 점프가 나왔습니다.

### 4. decomposition + routing

- `a100`
- `a101`

최근에는 문제를

- baseline
- scale
- routed deviation

으로 다시 분해하고, `soft routing`으로 expert를 고르는 구조가 메인입니다.

## 현재 최고 기록

- 파일: `submission_a101_10.csv`
- 점수: `10.1064209775`
- 날짜: `2026-04-21`

## 현재 메인 판단

지금은 `a94 family`를 더 미세하게 다듬는 것보다 `a100 family`를 더 안정적으로 운영하는 쪽이 중요합니다.

구체적으로는 아래가 핵심입니다.

1. baseline / scale 안정화
2. z-space expert 유지
3. soft routing 유지
4. support/testlike는 보조 feature로만 사용
5. hard subset mask보다 expert 재학습과 worst-group 검증 강화

즉 지금 병목은 backbone 부족보다, 어려운 샘플에서 어떤 expert를 얼마나 믿을지를 정하는 시스템 쪽에 더 가깝습니다.
