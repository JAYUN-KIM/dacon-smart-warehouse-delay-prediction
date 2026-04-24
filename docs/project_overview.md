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

같은 시나리오 안의 25개 슬롯을 하나의 sequence처럼 보는 접근이 중요하다고 판단하고 있습니다.

## 문제 해석

현재는 이 문제를 아래 4개 층으로 나눠서 보고 있습니다.

1. `scenario baseline`
   - 시나리오 전체의 기본 지연 수준
2. `scenario scale`
   - 시나리오 내부 변동성 크기
3. `slot deviation`
   - 각 슬롯이 baseline에서 얼마나 벗어나는지
4. `OOD / shift regime`
   - seen / unseen layout
   - 운영 상태 분포 이동
   - high-pressure / high-delay / high-shift 구간

## 핵심 EDA 해석

### 1. baseline 비중이 크다

전체 variance에서 scenario baseline 비중이 크기 때문에, row target을 바로 맞추는 것보다 baseline을 먼저 안정적으로 잡는 것이 중요하다고 보고 있습니다.

### 2. layout ID 자체보다 운영 상태 shift가 중요하다

중요하게 보고 있는 변수는 아래와 같습니다.

- `order_inflow_15m`
- `robot_active`
- `unique_sku_15m`
- `pack_pressure`
- `work_pressure`
- `pack_utilization`
- `low_battery_ratio`

즉 layout 자체보다 운영 패턴 분포가 달라질 때 성능이 흔들리는 구조에 더 가깝다고 보고 있습니다.

### 3. slot deviation은 시간축 + 압력 변수 영향이 크다

슬롯 단위 편차에는 아래 변수가 크게 작용합니다.

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

### 2. specialist 계열

- `a88`
- `a94`

representation residual, scenario baseline, shift/high/unseen specialist를 결합해 `a94_51 = 10.1133848903`까지 개선했습니다.

### 3. decomposition + routing

- `a100`
- `a101`

최근에는 문제를
- baseline
- scale
- routed deviation

으로 다시 분해하고, soft routing으로 expert를 선택하는 구조가 메인입니다.

## 현재 최고 기록

- 파일: `submission_a101_10.csv`
- 점수: `10.1064209775`
- 날짜: `2026-04-21`

## 최근 핵심 교훈

### correction layer는 반복적으로 public에서 실패

- `a102`
- `a104`
- `a105`
- `a106`

모두 로컬에서는 개선처럼 보였지만 public에서는 `a101_10`을 넘지 못했습니다.

현재 해석:
- backbone 문제가 아니라
- correction trigger / mask / magnitude calibration 문제가 큼

### expert 재학습은 더 건강한 방향

`a107`은 correction layer를 더 얹지 않고 `shift-heavy expert` 자체를 다시 학습한 실험이었습니다.

- `a101` direct router OOF: `7.4224`
- `a107` direct router OOF: `7.4162`
- public: `10.1067154934`

의미:
- correction layer 추가보다 expert 재학습 쪽이 더 안정적
- 다만 아직 public을 뒤집을 정도의 차이는 아님

### pseudo-group는 조심해서 써야 한다

`a108`에서 pseudo-group 기반 shift expert를 실험했습니다.

중간에 scenario hardness를 feature에 직접 넣었다가 leakage-like 착시를 확인했고, 이를 제거한 뒤 다시 검증했습니다.

수정 후 결과:
- `a108` direct router OOF: `7.4219`
- public: `10.1122539111`

의미:
- pseudo-group 방향 자체는 가능성 있음
- 하지만 현재 구현은 아직 제출용 카드가 아님
- hardness는 feature가 아니라 weighting/selection 보조로만 써야 안전함

## 현재 메인 판단

1. `a100 family`는 맞았다.
2. `a101_10`은 여전히 가장 강한 public 앵커다.
3. correction layer를 더 얹는 방향은 당분간 우선순위를 낮춘다.
4. 다음은 `shift-heavy expert` 재학습과 `worst-group / adversarial subset` 중심 검증 강화가 중요하다.

즉 지금은 모델을 갈아엎는 단계가 아니라, `a100 family`를 public 기준으로 더 안전하게 운영할 수 있게 validation과 expert 학습 기준을 바꾸는 단계입니다.
