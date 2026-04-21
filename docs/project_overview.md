# 프로젝트 개요

## 대회 목표

- 대회명: 데이콘 스마트 창고 출고 지연 예측 AI 경진대회
- 목표: `avg_delay_minutes_next_30m` 예측
- 평가 지표: `MAE`

## 데이터 구조

- Train: `10,000` 시나리오 × `25` 타임슬롯 = `250,000`행
- Test: `2,000` 시나리오 × `25` 타임슬롯 = `50,000`행
- Layout:
  - train layout: `250`
  - test layout: `100`
  - seen layout: `50`
  - test-only layout: `50`

## 문제 해석

이 문제는 단순한 row-wise 회귀보다 아래 구조로 보는 쪽이 더 맞다고 판단하고 있습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `scenario scale`
   - 시나리오 내부 변동 폭
3. `slot deviation`
   - 각 시점이 baseline에서 얼마나 벗어나는지
4. `OOD / shift regime`
   - unseen layout
   - high-pressure / high-delay
   - 운영 분포 이동이 큰 구간

## EDA에서 얻은 핵심

### 1. baseline 비중이 크다

전체 분산 중 scenario-level baseline 비중이 큽니다.
그래서 row target만 직접 맞추는 방식은 한계가 빨리 왔습니다.

### 2. layout ID보다 운영 상태 분포 이동이 더 중요하다

특히 아래 축이 중요했습니다.

- `order_inflow_15m`
- `robot_active`
- `unique_sku_15m`
- `pack_pressure`
- `work_pressure`
- `low_battery_ratio`

즉, layout 자체보다 운영 상태의 regime 변화가 더 중요합니다.

### 3. slot deviation은 시간축과 압력 변수의 영향이 크다

중요한 축은 다음과 같습니다.

- `time_idx`
- `time_remaining`
- `pack_pressure`
- `robot_active`
- `order_inflow_15m`

## 모델 흐름 요약

### 1. 초기 strong ensemble

- LGBM
- Transformer
- LSTM
- STT
- TransLF

### 2. residual stack

- 강한 앵커 위에 residual correction을 얹는 구조
- `a75 ~ a81`

### 3. layout-aware / sequence-aware 확장

- `a82`, `a83`

### 4. representation + shift specialist

- `a88`
- representation 신호를 shift subset에만 적용

### 5. integrated shift specialist

- `a94`
- representation residual + scenario baseline + combo specialist 통합

### 6. decomposition + routing

- `a100`
- `a101`

현재 가장 중요한 축은 이쪽입니다.

## 현재 핵심 방향

지금은 “평균적으로 가장 잘 맞는 모델 하나”를 더 찾는 단계가 아니라,

**어떤 샘플에서 어떤 expert가 덜 틀리는지 고르는 시스템**

을 만드는 단계입니다.

현재 주력 구조:

- baseline head
- scale head
- z-space expert library
- soft router
- confidence fallback

## 현재 최고 기록

- `submission_a101_10.csv`
- `10.1064209775`
- 날짜: `2026-04-21`
