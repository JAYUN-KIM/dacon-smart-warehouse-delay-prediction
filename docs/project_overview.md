# 프로젝트 개요

## 대회

- 대회명: 데이콘 스마트 창고 출고 지연 예측 AI 경진대회
- 목표: `avg_delay_minutes_next_30m` 예측
- 평가지표: `MAE`

## 데이터 구조

- Train: `10,000` 시나리오 × `25` 타임슬롯 = `250,000`행
- Test: `2,000` 시나리오 × `25` 타임슬롯 = `50,000`행
- Layout:
  - train layout: `250`
  - test layout: `100`
  - seen layout: `50`
  - test-only layout: `50`

## 지금까지의 문제 해석

이 문제는 단순 row-wise 회귀보다 아래 구조가 더 중요하다고 보고 있습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `slot deviation`
   - 시간대별 편차
3. `shift regime`
   - unseen / high cluster / 분포 이동이 큰 subset

최근 EDA에서는:

- 전체 분산 중 scenario mean 비중이 큼
- test-only layout shift는 `order_inflow`, `robot_active`, `unique_sku` 축에서 특히 큼
- scenario mean은 `low_battery_ratio`, `pack_utilization`, `pack_pressure`, `work_pressure`가 강하게 설명
- slot deviation은 `time_idx`, `time_remaining`, `pack_pressure`, `robot_active`, `order_inflow_15m` 영향이 큼

## 모델 흐름

### 1단계: 강한 베이스 만들기

- LightGBM
- Transformer
- LSTM
- STT
- TransLF

### 2단계: residual stack

- `a75 ~ a81`
- 강한 앵커를 유지하고 오차만 학습

### 3단계: layout / sequence 확장

- `a82`, `a83`

### 4단계: representation + shift specialist

- `a87`
- `a88`
- `a89 ~ a96`

이 단계에서 가장 큰 의미가 있었던 건:

- representation-derived signal은 전체보다 `shift subset`에서 잘 먹음
- `shift + high cluster + unseen`을 같이 본 `combo specialist`가 가장 강했음

## 현재 최고 방향

현재 가장 유효한 가설은:

- `a94 family`를 유지
- `combo regime` 정의를 더 안정적으로 만들기
- 필요한 경우 완전히 다른 signal source를 하나 더 붙이기

즉, 지금은 “low-band만 더 미세하게”가 아니라
“어떤 구간에 어떤 specialist를 적용할지”가 핵심입니다.

