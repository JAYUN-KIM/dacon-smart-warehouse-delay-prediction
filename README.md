# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 `스마트 창고 출고 지연 예측` 경진대회를 진행하며 쌓은 실험 방향과 판단 근거를 한국어로 정리한 포트폴리오 저장소입니다.

이 저장소는 단순히 점수만 남기기보다, 아래 내용을 날짜별로 기록하고 최종 회고까지 남기는 것을 목표로 했습니다.

- 어떤 문제 정의로 접근했는지
- 어떤 모델과 피처를 시도했는지
- 어떤 실험이 public 점수 개선으로 이어졌는지
- 어떤 실험은 local OOF에서 좋아 보여도 public에서 실패했는지
- 왜 특정 방향을 채택하거나 버렸는지

## 최종 최고 기록

- 최고 public MAE: `10.0038814352`
- 제출 파일: `submission_a156_046.csv`
- 기록 날짜: `2026-05-04`
- 핵심 해석: 마지막에는 단순 tail uplift가 아니라 `next_30m` 문제 정의로 돌아가, 미래 1~2 slot 정보를 현재 예측으로 당기는 phase-lead 구조와 public에서 먹힌 tail 분포 복원을 결합했습니다.

## 최종 회고

초반에는 ensemble, residual model, `baseline + scale + routed_z` 구조로 점수를 줄였습니다. 중반에는 late/high-stress underprediction 보정이 효과를 냈지만, 10.09 부근부터는 미세조정만으로 개선 폭이 너무 작아졌습니다.

2026-05-02부터는 기존 제출 예측을 그대로 anchor로 쓰는 방식에서 벗어나, raw train/test/layout 기반의 미래창 피처, 창고 압력 피처, scenario aggregate 피처를 대폭 확장했습니다. 이 축에서 `a137`, `a138`이 크게 먹혔고, 2026-05-03에는 future-pressure slot redistribution을 본격적으로 적용해 `a145_4830`이 `10.010757563`까지 내려갔습니다.

2026-05-04에는 마지막 제출을 앞두고 다시 원점으로 돌아가 문제 정의를 재해석했습니다. 예측 대상이 현재 지연이 아니라 향후 30분 평균 지연이라는 점에 집중해, 같은 scenario 안에서 앞으로 1~2 slot의 예측 및 운영 압력 신호를 현재 slot으로 당겨오는 `future phase-lead` 구조를 만들었습니다. 이후 public에서 검증된 `a155_481`의 꼬리 분포를 기준으로 마지막 도박 후보를 만들었고, 최종 `submission_a156_046.csv`가 public `10.0038814352`를 기록했습니다.

최종적으로 얻은 결론은 다음과 같습니다.

- 단순 모델 교체보다, 미래 운영 압력과 슬롯별 지연 재분배 구조가 더 큰 개선을 만들었습니다.
- scenario 평균은 크게 흔들지 않고, 같은 scenario 안에서 어느 슬롯을 더 올리고 내릴지 조절하는 방식이 public에 잘 맞았습니다.
- 마지막에는 public 검증 후보를 anchor로 두되, 문제 정의에 맞는 미래 phase 보정과 tail calibration을 결합하는 방식이 가장 강했습니다.
- 목표였던 9점대에는 닿지 못했지만, 초기 `11.83`에서 최종 `10.0038814352`까지 약 `1.8261` MAE를 줄였습니다.

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
| a145_4830 | `10.010757563` | scenario 평균 보존형 slot redistribution |
| a149_009 | `10.0073867868` | public-guided extrapolation |
| a151_886 | `10.0068002221` | queueing/domain reallocation |
| a155_481 | `10.0046018208` | future phase-lead + tail 복원 |
| a156_046 | `10.0038814352` | 최종 public-tail gamble |

## 최종 정리

이번 대회는 다음 흐름으로 마무리했습니다.

- 모델 family 탐색: CatBoost, LightGBM, sequence model, residual ensemble, MoE routing
- 구조 분해: scenario baseline, scale, standardized deviation, expected-error router
- OOD 대응: support/testlike feature, pseudo-group, shift-heavy expert, hard routing 실패 분석
- 원점 재해석: 미래창 feature, 창고 압력 feature, raw-only reboot, slot redistribution
- 최종 도박: next-30m phase-lead와 public-tail calibration 결합

가장 큰 교훈은 평균적으로 좋은 모델을 하나 더 만드는 것보다, 대회 문제 정의에 맞춰 “미래 압력이 어느 슬롯에서 지연으로 나타나는지”를 예측 분포에 반영하는 것이 더 중요했다는 점입니다. 최종 목표였던 9점대에는 닿지 못했지만, 마지막 제출까지 문제를 다시 해석하고 실험 근거를 남긴 프로젝트로 정리했습니다.

## 문서 구성

- [포트폴리오 케이스 스터디](docs/portfolio_case_study.md)
- [이력서 / 포트폴리오 요약](docs/resume_summary.md)
- [다른 AI에게 전달할 정리 프롬프트](docs/ai_handoff_prompt.md)
- [프로젝트 개요](docs/project_overview.md)
- [실험 로그](docs/experiment_log.md)
- [일일 리포트](docs/daily_report.md)
- [최종 연구 요약](docs/final_research_summary.md)
- [날짜별 작업 기록](docs/daily_logs/)
- [public 점수 로그](docs/public_score_log.json)
