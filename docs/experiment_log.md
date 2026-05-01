# 실험 로그

## 현재 최고 기록

- 최고 제출: `submission_a131_101.csv`
- Public MAE: `10.0920140626`
- 기준일: `2026-05-01`
- 핵심 방향: late/high-stress 보정축을 유지하되, 포화 신호가 나온 뒤 from-scratch direct LGBM signal을 낮은 비율로 흡수

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
| a128 | `submission_a128_001.csv` | 10.0939941912 | public-safe late blend로 10.093대 진입 |
| a129 | `submission_a129_001.csv` | 10.0939015979 | scenario-relative shift 보정으로 미세 개선 |
| a130 | `submission_a130_002.csv` | 10.0946330552 | scenario offset pivot은 public에서 악화 |
| a131 | `submission_a131_101.csv` | 10.0920140626 | raw direct LGBM signal microblend로 새 최고점 |

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

### a128

- 대표 제출: `submission_a128_001.csv`
- Public MAE: `10.0939941912`
- 기준 anchor: `a127_003`
- 해석: 기존 late/high-stress 보정축을 public-safe하게 한 번 더 밀어 10.093대에 진입했다.

### a129

- 대표 제출: `submission_a129_001.csv`
- Public MAE: `10.0939015979`
- 핵심 방향: scenario-relative shift 보정
- 해석: 개선폭은 작지만 기존 축이 아직 완전히 죽지는 않았음을 확인했다.

### a130

- 대표 제출: `submission_a130_002.csv`
- Public MAE: `10.0946330552`
- 핵심 방향: scenario offset pivot
- 해석: 공격적인 scenario offset 보정은 public에서 악화됐다. 같은 축을 더 세게 미는 방식은 포화 및 overfit 위험이 크다.

### a131

- 대표 제출: `submission_a131_101.csv`
- Public MAE: `10.0920140626`
- 생성 코드: `model_a131_from_scratch_direct.py`
- 핵심 방향: 기존 제출 예측이나 anchor를 feature로 쓰지 않고 raw train/test와 layout_info로 direct LGBM family를 새로 구성
- 검증 결과: row-level direct LGBM OOF는 `8.7876`, row quantile OOF는 `8.8116`, scenario-slot direct OOF는 `8.8324`
- 주의점: scenario-slot direct는 OOF는 괜찮지만 test mean이 `6.19`로 비정상적으로 낮아 제출 위험 후보로 분류했다.
- 해석: pure direct 단독 제출이 아니라 `a129_001` anchor에 row direct signal을 1.5%만 흡수한 microblend가 가장 실전적으로 유효했다.

## 현재 결론

- late/high-stress uplift 축은 아직 살아 있지만, 단순 강화는 포화 신호가 있다.
- `a130`처럼 scenario offset을 크게 밀면 public에서 악화될 수 있다.
- 기존 계열과 다른 raw direct signal은 단독보다 microblend로 쓸 때 더 안전하다.
- OOF가 좋아도 test prediction 분포가 무너지면 제출 후보에서 제외해야 한다.
- 현재는 anchor refinement와 새 direct signal 흡수를 병행하는 것이 가장 기대값이 높다.

## 다음 실험 방향

`a132` 권장 방향:

- `a131_101`을 anchor로 사용
- row direct LGBM alpha를 `0.010~0.035` 범위에서 좁게 탐색
- direct quantile signal은 보조 신호로만 제한
- slot-direct 계열은 test mean mismatch 때문에 제외
- late/high-stress mask와 direct signal이 같은 방향인 구간에서 selective correction 시도
- 평균 예측값과 test max가 기존 최고 분포에서 크게 벗어나지 않는 후보만 제출 후보로 유지

## 메모

오늘의 핵심은 완전히 새로 만든 direct model을 단독으로 쓰는 것이 아니라, 기존 최고 anchor에 낮은 비율로 흡수했을 때 실제 public 개선이 발생했다는 점이다. 9점대 진입을 위해서는 기존 보정축을 유지하면서도 상관이 낮은 새 신호를 계속 만들어 안전하게 섞는 전략이 필요하다.
