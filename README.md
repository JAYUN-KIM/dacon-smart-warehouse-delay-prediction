# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하며, 실험 방향과 판단 근거를 한국어로 정리해 둔 포트폴리오 저장소입니다.

이 저장소의 목적은 단순히 점수만 기록하는 것이 아니라, 아래 내용을 날짜별로 남기는 것입니다.

- 어떤 문제 정의로 접근했는지
- 어떤 모델과 피처를 시도했는지
- 어떤 실험이 public 점수 개선으로 이어졌는지
- 어떤 실험은 local OOF에서는 좋아 보였지만 public에서 실패했는지
- 다음 실험 방향을 어떻게 정했는지

## 현재 최고 기록

- 최고 public 점수: `10.0941228322`
- 제출 파일: `submission_a127_003.csv`
- 기록 날짜: `2026-04-30`
- 핵심 해석: late/high-stress 구간의 과소예측 보정축이 계속 유효했고, `q=0.900` coverage 10%를 유지한 채 평균 uplift와 late profile을 조금씩 강화하는 방식이 public에서 연속 개선을 만들었습니다.

## 현재 핵심 판단

초반에는 강한 ensemble과 residual model을 중심으로 점수를 줄였고, 중반에는 `baseline + scale + routed deviation` 구조로 문제를 분해했습니다. 이후 `a114`부터 future-window 기반 warehouse pressure와 late-slot 관점이 효과를 보였고, `a122` 이후에는 late/high-stress 구간 과소예측 보정이 가장 강한 개선축으로 확인됐습니다.

최근의 핵심 흐름은 다음과 같습니다.

- `a122`: late/high-stress 구간에 작은 uplift를 적용해 `10.0967991272` 달성
- `a124`: flat uplift를 late-weighted shift로 바꿔 `10.0960054075` 달성
- `a125`: a124보다 조금 이른 시작과 더 큰 평균 uplift로 `10.0953184117` 달성
- `a126`: 평균 uplift를 `0.0600`까지 밀어 `10.0946609016` 달성
- `a127`: 평균 uplift `0.0630`, max uplift 약 `1.04` 근처 후보로 `10.0941228322` 달성

즉 현재 방향은 새 backbone을 무작정 바꾸는 것이 아니라, public이 반응한 late/high-stress underprediction 보정축을 더 정밀하게 조절하는 것입니다.

## 주요 점수 흐름

| 단계 | public | 핵심 내용 |
| --- | ---: | --- |
| baseline | `11.83` | 초기 기준선 |
| a88 | `10.1201425252` | representation 기반 shift expert |
| a94 | `10.1133848903` | scenario baseline + shift/high/unseen specialist |
| a100 | `10.1090848449` | baseline + scale + routed deviation 구조 |
| a101 | `10.1064209775` | soft router와 fallback 적용 |
| a114 | `10.103316418` | future-window scenario baseline/scale 강화 |
| a117 | `10.1005923422` | clipped ridge seq2seq delta를 앵커에 작게 반영 |
| a122 | `10.0967991272` | late/high-stress 과소예측 구간 small uplift 적용 |
| a124 | `10.0960054075` | flat uplift를 late-weighted stress shift로 개선 |
| a125 | `10.0953184117` | public-guided late shift 강화 |
| a126 | `10.0946609016` | a125 anchor 기준 mean uplift 추가 강화 |
| a127 | `10.0941228322` | q=0.900 유지, 평균 uplift 0.063 부근으로 추가 개선 |

## 문서 구성

- [프로젝트 개요](docs/project_overview.md)
- [실험 로그](docs/experiment_log.md)
- [일일 리포트](docs/daily_report.md)
- [날짜별 작업 기록](docs/daily_logs/)
- [public 점수 로그](docs/public_score_log.json)
