# 실험 로그

## 현재 최고 기록

- 최고 제출: `submission_a127_003.csv`
- Public MAE: `10.0941228322`
- 기준일: `2026-04-30`
- 핵심 방향: late/high-stress 구간의 과소예측을 `q=0.900` coverage 안에서 점진적으로 보정

## 주요 점수 흐름

| 단계 | 제출 | Public MAE | 해석 |
| --- | --- | ---: | --- |
| 초기 | `baseline` | 11.83 | 제출/파이프라인 기준선 |
| a48 | `submission_a48_v4_3.csv` | 10.1477 | 초기 앙상블로 10.1대 진입 |
| a88 | `submission_a88_27.csv` | 10.1201425252 | representation residual 및 shift/high/unseen specialist 방향 |
| a94 | `submission_a94_51.csv` | 10.1133848903 | scenario baseline signal 통합으로 큰 폭 개선 |
| a100 | `submission_a100_05.csv` | 10.1090848449 | baseline + scale + routed_z 구조 검증 |
| a101 | `submission_a101_10.csv` | 10.1064209775 | soft expected-error router 최고점 |
| a114 | `submission_a114_09.csv` | 10.103316418 | 미래창/pressure 피처 확장으로 개선 |
| a117 | `submission_a117_09.csv` | 10.1005923422 | late/high-pressure uplift 계열 유효성 확인 |
| a122 | `submission_a122_1045.csv` | 10.0967991272 | late pressure uplift로 10.09대 진입 |
| a124 | `submission_a124_1443.csv` | 10.0960054075 | late-shift mean-preserving uplift로 최고점 갱신 |
| a125 | `submission_a125_001.csv` | 10.0953184117 | public-guided late shift 강화 |
| a126 | `submission_a126_001.csv` | 10.0946609016 | mean uplift 0.060까지 강화 |
| a127 | `submission_a127_003.csv` | 10.0941228322 | 중간 강도 push가 추가 개선 |

## 최근 실험 상세

### a125

- 대표 제출: `submission_a125_001.csv`
- Public MAE: `10.0953184117`
- 기준 anchor: `a124_1443`
- 핵심 파라미터: `q=0.900`, `target_mean=0.0575`, `floor=0.40`, `start=11.5`, `denom=7.5`, `power=0.65`
- 해석: a124보다 조금 더 이른 시작과 더 큰 평균 uplift를 public이 받아줬다.

### a126

- 대표 제출: `submission_a126_001.csv`
- Public MAE: `10.0946609016`
- 기준 anchor: `a125_001`
- 핵심 파라미터: `q=0.900`, `target_mean=0.0600`, `floor=0.37`, `start=11.25`, `denom=7.0`, `power=0.50`
- 해석: 평균 uplift를 한 단계 더 높여도 public이 개선됐다.

### a127

- 대표 제출: `submission_a127_003.csv`
- Public MAE: `10.0941228322`
- 기준 anchor: `a126_001`
- 핵심 파라미터: `q=0.900`, `target_mean=0.0630`, `floor=0.335`, `start=10.75`, `denom=6.50`, `power=0.45`
- 해석: 더 강한 후보 중에서도 중간 강도 후보가 가장 균형적으로 개선됐다.

## 현재 결론

- late/high-stress uplift 축은 아직 살아 있다.
- coverage를 넓히기보다, 현재 10% 고위험 구간 안에서 보정 shape를 조정하는 것이 더 효율적이다.
- 개선폭은 줄고 있으므로 다음부터는 무작정 더 올리기보다 test max와 max uplift를 관리해야 한다.
- a128은 a127_003 주변에서 아주 좁게 탐색하는 것이 맞다.

## 다음 실험 방향

`a128` 권장 범위:

- `q`: `0.900` 우선 고정
- `target_mean`: `0.0625~0.0645`
- `floor`: `0.335~0.350`
- `start`: `10.75~11.00`
- `denom`: `6.50~6.75`
- `power`: `0.42~0.50`
- max uplift: `1.03~1.06`
- test max: 가능하면 `45.04` 근처 이하 우선

## 메모

오늘의 개선은 크지는 않지만, 같은 구조 축에서 3회 연속 public 개선이 나왔다는 점이 중요하다. 9점대 진입까지는 더 큰 레버가 필요할 수 있으나, 현재 남은 제출에서는 이 축을 정밀하게 더 다듬는 것이 가장 기대값이 높다.
