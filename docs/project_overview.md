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

현재는 이 문제를 아래 5개 층으로 나눠서 보고 있습니다.

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
5. `future-window stress`
   - 같은 시나리오 안에서 가까운 미래 슬롯의 부하/압력/배터리 악화가 어떻게 전개되는지

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

### 4. 미래 부하 해석은 실제 신호다

후반부 실험에서 확인한 가장 중요한 교훈은, 이 문제가 단순한 현재 상태 회귀가 아니라는 점입니다.

- 같은 시나리오 안에서 이미 주어진 25개 슬롯 전체를 활용할 수 있고
- 가까운 미래의 주문 유입, 압력, 배터리 악화가 실제 지연에 강하게 연결됩니다

즉 `lead1`, `fut2`, `fut3`, `future_stress_score` 같은 피처는 실제 backbone 신호가 될 가치가 있습니다.

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

문제를
- baseline
- scale
- routed deviation

으로 다시 분해하고, soft routing으로 expert를 선택하는 구조가 메인이 되었습니다.

### 4. future-window 계열

- `a110`: 미래 부하 해석을 처음 backbone에 반영
- `a112`: 미래창 피처 과확장 실패
- `a113`: compact row future도 실패
- `a114`: 미래창을 scenario baseline/scale 강화용으로 넣어 당시 최고 public 달성
- `a115`: `a114` backbone 유지 + 후보 생성 정밀화, 로컬은 좋아졌지만 public은 `a114` 미달

### 5. clipped ridge delta 계열

- `a116`: scenario-level ridge seq2seq direct family 실험
- `a117`: ridge direct prediction과 `a114` 앵커의 차이를 clipped delta로 얇게 반영해 새 최고 public 달성
- `a118`: `a117_09`의 안전한 분포 대역을 기준으로 positive/negative delta를 비대칭 클리핑했지만 public 개선 실패
- `a119`: `a117_09` 초근접 microgrid를 제출했지만 public 개선 실패

이 계열의 핵심은 direct model을 그대로 믿지 않는 것입니다. 약한 direct prediction이라도 기존 앵커와 다른 방향의 delta를 제공할 수 있고, 이 delta를 낮은 alpha와 clipping으로 제한할 때 `a117_09`에서 실제 public 개선이 나왔습니다. 다만 `a118`, `a119` 결과를 보면 같은 delta family는 `a117_09` 근처에서 거의 포화된 것으로 보고 있습니다.

## 현재 최고 기록

- 파일: `submission_a117_09.csv`
- 점수: `10.1005923422`
- 날짜: `2026-04-27`

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
- 다만 아직 public을 뒤집을 정도의 차이는 아니었음

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

### validation과 선택 기준만 바꾸는 것으로는 부족하다

`a109`에서는 단순한 물리 extreme expert와 `worst-group / testlike / baseline_hi` 중심 선택 기준으로 다시 정리했습니다.

- public: `10.1085982977`

의미:
- validation을 바꾸는 방향은 맞음
- 하지만 selection 기준만 바꾸는 것으로는 `a101_10`을 뒤집기 어렵다는 점을 확인

### future-window는 “많이”보다 “정확하게”가 중요하다

`a112`에서 피처를 300개 이상까지 늘렸지만 오히려 악화됐고, `a113`도 row 확장형 future backbone으로는 개선이 없었습니다.

반대로 `a114`는 미래창 신호를 scenario baseline/scale에 집중해서 넣었고, 당시 public 최고 기록을 만들었습니다.

즉:
- future-window 해석은 맞음
- 하지만 row expert 쪽으로 무한정 늘리는 건 오히려 독
- scenario-level stress 해석으로 넣을 때 가장 잘 작동함

## 현재 메인 판단

1. `a100 family`와 `a114`의 future-window scenario 해석은 맞았다.
2. `a117_09`가 현재 가장 강한 public 앵커다.
3. correction layer를 더 얹는 방향은 당분간 우선순위를 낮춘다.
4. future-window 신호는 유지하되, scenario-level stress 해석에 집중한다.
5. `a116` ridge seq2seq direct model은 단독으로 약하지만 delta provider로 한 번 가치를 보였다.
6. 하지만 `a118`, `a119` 결과상 clipped ridge delta 추가 미세조정은 우선순위를 낮춘다.
7. 다음은 `a117_09`가 구조적으로 틀리는 high-error scenario group을 다시 찾는 것이다.

즉 지금은 `a117_09`를 기준 앵커로 두고, 같은 delta band를 더 깎는 단계가 아니라 앵커의 실패 구간을 다시 정의하는 단계입니다.
