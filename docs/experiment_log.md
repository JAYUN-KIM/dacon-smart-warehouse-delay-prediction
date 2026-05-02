# 실험 로그

## 현재 최고 기록

- 최고 제출: `submission_a138_147.csv`
- Public MAE: `10.0265043299`
- 기준일: `2026-05-02`
- 핵심 방향: 기존 late/high-stress 보정축의 포화를 인정하고, 이전 제출 예측을 모델 입력으로 쓰지 않는 raw-only reboot ensemble로 전환

## 주요 점수 흐름

| 단계 | 제출 | Public MAE | 해석 |
| --- | --- | ---: | --- |
| 초기 | `baseline` | 11.83 | 제출/파이프라인 기준선 |
| a48 | `submission_a48_v4_3.csv` | 10.1477 | 초기 앙상블로 10.1대 진입 |
| a88 | `submission_a88_27.csv` | 10.1201425252 | representation residual 및 shift/high/unseen specialist 방향 |
| a94 | `submission_a94_51.csv` | 10.1133848903 | scenario baseline signal 통합으로 큰 개선 |
| a100 | `submission_a100_05.csv` | 10.1090848449 | baseline + scale + routed_z 구조 검증 |
| a101 | `submission_a101_10.csv` | 10.1064209775 | soft expected-error router 계열 최고점 |
| a114 | `submission_a114_09.csv` | 10.103316418 | 미래창 pressure 피처 확장으로 개선 |
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
| a132 | `submission_a132_002.csv` | 10.0913986125 | direct signal refinement |
| a133 | `submission_a133_104.csv` | 10.0905078248 | direct alpha gamble로 10.090대 접근 |
| a135 | `submission_a135_003.csv` | 10.0901537375 | ranker signal blend로 추가 개선 |
| a137 | `submission_a137_011.csv` | 10.02829 | raw-only reboot ensemble이 대형 점프 |
| a138 | `submission_a138_147.csv` | 10.0265043299 | raw-only fine grid로 현재 최고점 |

## 최근 실험 상세

### a132

- 대표 제출: `submission_a132_002.csv`
- Public MAE: `10.0913986125`
- 해석: a131 이후 direct signal refinement가 소폭 개선을 만들었지만, 9점대 진입을 위한 큰 레버는 아니었다.

### a133

- 대표 제출: `submission_a133_104.csv`
- Public MAE: `10.0905078248`
- 해석: alpha를 더 과감하게 탐색해 10.090대까지 접근했다. 다만 개선폭은 여전히 작아 기존 축 포화 신호가 강했다.

### ranker 코드 점검

- 입력 코드: `dacon_236696_ranker.py`
- 수정 포인트: 명시적인 시간/slot 컬럼이 없을 때 운영 변수를 시간 정렬 기준으로 오인할 수 있어 `ID` 순서를 우선 사용하도록 수정
- 검증:
  - smoke fixed OOF MAE: `9.11882`
  - LGB 5-fold ranker OOF MAE: `8.89765`
- 해석: public code나 외부 아이디어는 그대로 사용하지 않고, 정렬/누수/규정 관점에서 확인해야 한다.

### a135

- 대표 제출: `submission_a135_003.csv`
- Public MAE: `10.0901537375`
- 해석: ranker signal을 섞어 개선했지만, 기존 anchor 중심 조합에서는 여전히 10.09 부근에 묶였다.

### a136/a137

- 생성 코드:
  - `model_a136_domain_reboot.py`
  - `model_a137_raw_reboot_ensemble.py`
- 핵심: 이전 제출 예측을 모델 입력으로 쓰지 않고 raw train/test/layout_info 기반의 domain/future/scenario feature와 ranker를 결합
- 검증:
  - a136 OOF MAE: `8.609878597985363`
  - ranker OOF MAE: `8.89765201581869`
  - a137 candidate OOF MAE: `8.58505361649153`
- 대표 제출: `submission_a137_011.csv`
- Public MAE: `10.02829`
- 해석: 기존 축을 더 미는 것이 아니라 raw-only family로 재시작한 것이 가장 큰 개선을 만들었다.

### a138

- 생성 코드: `model_a138_raw_reboot_finegrid.py`
- 대표 제출: `submission_a138_147.csv`
- Public MAE: `10.0265043299`
- 후보 설명: `w_a136_0.82_center_p80_alpha_1.010`
- OOF MAE: `8.584451426707153`
- 예측 분포:
  - mean: `19.776156630979433`
  - std: `14.545700562359132`
  - p50: `15.697762928549192`
  - p95: `39.620172096000964`
  - p99: `48.534802809912904`
  - max: `64.41252113067038`
- 해석: `a137_011`과 분포를 거의 유지하면서 OOF가 조금 더 나은 후보가 public에서도 추가 개선을 만들었다.

## 현재 결론

- late/high-stress uplift 축은 유효하지만 단독 미세 조정만으로는 9점대 진입이 어렵다.
- 큰 개선은 raw-only reboot family에서 나왔으므로, 다음 실험의 중심은 이 family여야 한다.
- 이전 제출 예측을 모델 입력으로 쓰지 않는 구조가 public에서 크게 먹혔고 private 안정성도 상대적으로 좋을 가능성이 있다.
- ranker/future-window/domain feature는 유망하지만, 시간 정렬과 test 활용 범위는 계속 이중 확인해야 한다.
- a138 이후에는 단순 fine grid보다 ranker diversity, scenario pressure feature, high-tail specialist를 추가하는 쪽이 기대값이 높다.

## 다음 실험 방향

`a139` 권장 방향:

- raw-only reboot pipeline 유지
- ranker model을 추가 다양화해 a136과의 error correlation 낮추기
- scenario-level queue/load/capacity feature 보강
- high-delay tail 전용 specialist 추가
- hard switch 대신 soft blend만 사용
- `a138_147` 성공 분포에서 크게 벗어나는 후보는 제출 제외

## 메모

오늘의 핵심은 `10.0920140626 -> 10.0265043299`의 큰 개선이다. 이 변화는 단순 보정 강화가 아니라 문제를 다시 보고 raw feature 기반의 새로운 family를 만든 결과다. 다음 목표는 이 방향을 유지하면서 10.00대가 아니라 9점대 진입까지 갈 수 있는 독립 신호를 하나 더 만드는 것이다.
