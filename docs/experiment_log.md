# 실험 로그

## 현재 최고 기록

- 점수: `10.0967991272`
- 파일: `submission_a122_1045.csv`
- 날짜: `2026-04-28`

## 주요 점수 흐름

| 실험 | public | 핵심 |
| --- | ---: | --- |
| baseline | `11.83` | 초기 기준선 |
| a48 | `10.1477` | 초기 ensemble |
| a56 | `10.1276` | STT + TransLF 계열 |
| a66 | `10.1260335184` | blend 비중 조정 |
| a75 | `10.122152212` | residual CatBoost |
| a88 | `10.1201425252` | representation 기반 shift expert |
| a94 | `10.1133848903` | scenario baseline + shift/high/unseen specialist |
| a100 | `10.1090848449` | baseline + scale + routed deviation |
| a101 | `10.1064209775` | soft expected-error router |
| a114 | `10.103316418` | future-window scenario baseline/scale 강화 |
| a117 | `10.1005923422` | clipped ridge seq2seq delta |
| a122 | `10.0967991272` | late/high-stress small uplift |

## 주요 실험 해석

### a88: representation 기반 shift expert

representation residual을 활용해 shift 구간을 더 잘 다루려는 실험입니다.

결과:
- public: `10.1201425252`

의미:
- 단순 평균 예측기보다, 어려운 운영 구간을 따로 보는 specialist 방향이 유효했습니다.

### a94: integrated shift specialist

`representation residual`, `scenario baseline`, `shift/high/unseen combo specialist`를 통합했습니다.

결과:
- public: `10.1133848903`

의미:
- baseline과 specialist를 함께 쓰는 방향이 큰 점프를 만들었습니다.

### a100: decomposition router

문제를 다음 구조로 분해했습니다.

```text
y_hat = baseline + scale * routed_z
```

결과:
- public: `10.1090848449`

의미:
- raw target을 바로 맞히기보다 baseline, scale, deviation을 나눠보는 접근이 맞았습니다.

### a101: soft router

expected-error 기반 soft router와 fallback을 적용했습니다.

결과:
- public: `10.1064209775`

의미:
- hard routing보다 soft routing이 더 안정적이었습니다.
- 이 시점까지는 decomposition + routing이 주력 family였습니다.

### a102 ~ a106: correction layer 계열

`a101` 앵커 위에 support-aware fallback, subset correction, continuous correction을 얹는 실험을 반복했습니다.

대표 결과:
- `a102_24 = 10.1360030381`
- `a104_15 = 10.1111502564`
- `a105_13 = 10.1074718609`
- `a106_20 = 10.11045386`

의미:
- local OOF에서는 좋아 보이는 경우가 있었지만 public에서 반복적으로 실패했습니다.
- correction layer가 local residual noise에 과적합되기 쉽다는 판단을 내렸습니다.

### a107 ~ a109: expert 재학습과 pseudo-group

correction layer 대신 shift-heavy expert 자체를 다시 학습하거나, pseudo-group을 정의해 어려운 구간을 강화했습니다.

대표 결과:
- `a107_10 = 10.1067154934`
- `a108_12 = 10.1122539111`
- `a109_09 = 10.1085982977`

의미:
- expert 재학습은 correction layer보다 건강한 방향이었지만, pseudo-group을 복잡하게 만들면 public에서 흔들렸습니다.

### a110 ~ a115: future-window 계열

같은 시나리오 내 25개 슬롯 전체를 활용해 가까운 미래의 부하와 압력 신호를 만들었습니다.

대표 결과:
- `a110_09 = 10.106859334`
- `a114_09 = 10.103316418`
- `a115_146 = 10.1066275842`

의미:
- future-window 신호는 유효했습니다.
- 다만 row-level feature를 무작정 늘리는 것보다 scenario baseline/scale을 강화하는 방식이 더 안정적이었습니다.
- `a114`가 이 방향의 가장 좋은 성과였습니다.

### a116 ~ a117: ridge seq2seq delta

`a116`에서는 scenario-level feature를 이용해 25개 슬롯 전체를 한 번에 예측하는 ridge seq2seq direct model을 만들었습니다.

직접 모델 자체는 약했지만, 기존 앵커와 다른 방향의 예측 delta를 제공했습니다.

`a117`에서는 이 delta를 작게 clipping해서 앵커에 반영했습니다.

결과:
- `submission_a117_09.csv`
- 설정: `alpha=0.08`, `q98 clip`
- OOF MAE: `7.7673277855`
- public: `10.1005923422`

의미:
- 약한 direct model도 앵커와 다른 방향의 정보를 주면 도움이 될 수 있습니다.
- 단, delta를 크게 반영하면 public에서 악화됐습니다.

### a118 ~ a120: a117 주변 포화 확인

`a118`은 asymmetric clipped delta, `a119`는 `a117_09` 근처 microgrid, `a120`은 scenario bias calibrator였습니다.

결과:
- `a118_01 = 10.1018318718`
- `a119_03 = 10.1010915332`
- `a120`은 local 개선폭이 너무 작아 미제출

의미:
- `a117_09` 근처의 단순 delta shape 조정은 포화됐습니다.
- 같은 family를 계속 미세 조정하는 것보다, `a117_09`가 구조적으로 틀리는 구간을 다시 찾는 것이 필요했습니다.

### a121: high-error group EDA

`a117_09`의 OOF residual을 기준으로 high-error scenario를 분석했습니다.

핵심 수치:
- scenario MAE top 10% threshold: `19.055895`
- high-error scenario mean MAE: `36.048248`
- rest scenario mean MAE: `4.625003`
- high-error scenario mean bias: `+26.686848`

주요 신호:
- late slot에서 오차와 positive bias가 커졌습니다.
- `pack_pressure` high q90: MAE lift `13.784`, bias `+10.598`
- `pack_utilization` high q90: MAE lift `10.610`, bias `+8.178`
- `future_stress_score` high q90: MAE lift `6.266`, bias `+5.166`

의미:
- high-error group은 단순 노이즈가 아니라 구조적 과소예측이었습니다.
- 이 분석이 `a122`의 직접적인 근거가 됐습니다.

### a122: late/high-stress small uplift

`a117_09`를 앵커로 유지하고, stress risk가 높은 일부 구간에만 작은 양수 보정을 적용했습니다.

대표 후보:
- `submission_a122_1045.csv`
- risk: `all_stress_small`
- bins: `10`
- stat: `median`
- shrink: `0.5`
- OOF MAE: `7.7663116455`
- test 평균 uplift: `0.054897`
- max uplift: `0.393809`

public:
- `10.0967991272`

의미:
- 처음으로 10.10 벽을 깼습니다.
- `a121`에서 찾은 late/high-stress 과소예측 축이 public에서도 유효하다는 점을 확인했습니다.

## 현재 결론

1. `a122_1045`가 현재 최고 public 앵커입니다.
2. clipped ridge delta micro tuning은 `a117_09` 근처에서 포화됐습니다.
3. correction layer를 넓게 얹는 방식은 여전히 위험합니다.
4. public이 반응한 축은 late/high-pressure/high-utilization/high-stress 구간의 작은 양수 보정입니다.
5. 다음 실험은 `a122_1045` family를 중심으로 risk score와 uplift 강도를 정밀 탐색하는 것이 가장 합리적입니다.
