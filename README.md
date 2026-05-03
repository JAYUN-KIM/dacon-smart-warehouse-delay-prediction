# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 `스마트 창고 출고 지연 예측` 경진대회를 진행하며, 실험 방향과 판단 근거를 한국어로 정리하는 포트폴리오 저장소입니다.

이 저장소는 단순히 점수만 남기기보다, 아래 내용을 날짜별로 기록하는 것을 목표로 합니다.

- 어떤 문제 정의로 접근했는지
- 어떤 모델과 피처를 시도했는지
- 어떤 실험이 public 점수 개선으로 이어졌는지
- 어떤 실험은 local OOF에서 좋아 보여도 public에서 실패했는지
- 다음 실험 방향을 어떻게 정했는지

## 현재 최고 기록

- 최고 public MAE: `10.010757563`
- 제출 파일: `submission_a145_4830.csv`
- 기록 날짜: `2026-05-03`
- 핵심 해석: 기존 late/high-stress 미세 보정 축에서 벗어나, raw feature 기반 대규모 미래창/도메인 피처와 scenario mean-preserving slot redistribution을 결합하면서 10.01 초반까지 크게 전진했습니다.

## 현재 판단

초반에는 ensemble, residual model, `baseline + scale + routed_z` 구조로 점수를 줄였습니다. 중반에는 late/high-stress underprediction 보정이 효과를 냈지만, 10.09 부근부터는 미세조정만으로 개선 폭이 너무 작아졌습니다.

2026-05-02부터는 기존 제출 예측을 그대로 anchor로 쓰는 방식에서 벗어나, raw train/test/layout 기반의 미래창 피처, 창고 압력 피처, scenario aggregate 피처를 대폭 확장했습니다. 이 축에서 `a137`, `a138`이 크게 먹혔고, 2026-05-03에는 future-pressure slot redistribution을 본격적으로 적용해 `a145_4830`이 `10.010757563`까지 내려갔습니다.

현재 가장 중요한 결론은 다음과 같습니다.

- 단순 모델 교체보다, 미래 운영 압력과 슬롯별 지연 재분배 구조가 더 큰 개선을 만들었습니다.
- scenario 평균은 크게 흔들지 않고, 같은 scenario 안에서 어느 슬롯을 더 올리고 내릴지 조절하는 방식이 public에 잘 맞았습니다.
- 9점대 진입을 위해서는 안전한 미세조정보다 `a145_4830`을 기준으로 더 공격적인 extrapolation 후보를 시험해야 합니다.

## 주요 점수 흐름

| 단계 | public MAE | 핵심 내용 |
| --- | ---: | --- |
| baseline | `11.83` | 초기 기준선 |
| a88 | `10.1201425252` | representation 기반 shift expert |
| a94 | `10.1133848903` | scenario baseline + specialist 통합 |
| a100 | `10.1090848449` | baseline + scale + routed deviation 구조 |
| a101 | `10.1064209775` | soft router와 fallback 적용 |
| a114 | `10.103316418` | future-window pressure 피처 확장 |
| a122 | `10.0967991272` | late/high-stress uplift로 10.09대 진입 |
| a127 | `10.0941228322` | late/high-stress 축 미세 개선 |
| a131 | `10.0920140626` | from-scratch direct signal 소량 흡수 |
| a135 | `10.0901537375` | ranker signal blend |
| a137 | `10.02829` | raw-only reboot ensemble로 큰 점프 |
| a138 | `10.0265043299` | raw-only fine grid |
| a139 | `10.0208783095` | 공격적 tail expert 계열 |
| a145_1755 | `10.0143960347` | future-pressure slot redistribution 성공 |
| a145_4830 | `10.010757563` | 현재 최고 기록 |

## 다음 실험 방향

다음 제출 가능 시점에는 `a145_4830`을 anchor로 두고 9점대 진입을 위한 도박 후보를 우선 시험합니다.

- 1순위 후보: `submission_a149_008.csv`
- 2순위 공격 후보: `submission_a149_009.csv`
- 안전 후보: `submission_a149_085.csv`

핵심은 평균 예측값을 크게 바꾸는 것이 아니라, public에서 먹힌 미래 압력 기반 슬롯 재분배 모양을 조금 더 강하게 밀어붙이는 것입니다.

## 문서 구성

- [프로젝트 개요](docs/project_overview.md)
- [실험 로그](docs/experiment_log.md)
- [일일 리포트](docs/daily_report.md)
- [날짜별 작업 기록](docs/daily_logs/)
- [public 점수 로그](docs/public_score_log.json)
