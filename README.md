# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하며, 실험 방향과 판단 근거를 한국어로 정리해 둔 포트폴리오 저장소입니다.

이 저장소의 목적은 단순히 점수만 기록하는 것이 아니라, 아래 내용을 날짜별로 남기는 것입니다.

- 어떤 문제 정의로 접근했는지
- 어떤 모델과 피처를 시도했는지
- 어떤 실험이 public 점수 개선으로 이어졌는지
- 어떤 실험은 local OOF에서는 좋아 보였지만 public에서 실패했는지
- 다음 실험 방향을 어떻게 정했는지

## 현재 최고 기록

- 최고 public 점수: `10.0967991272`
- 제출 파일: `submission_a122_1045.csv`
- 기록 날짜: `2026-04-28`
- 핵심 해석: `a117_09` 앵커가 과소예측하는 late/high-stress 구간을 아주 작게 양수 보정한 후보가 public에서 검증됨

## 현재 핵심 판단

초반에는 강한 ensemble과 residual model을 중심으로 점수를 줄였고, 중반에는 `baseline + scale + routed deviation` 구조로 문제를 분해했습니다. 이후 `a114`에서 future-window 기반 scenario stress 해석이 성과를 냈고, `a117`에서는 ridge seq2seq direct prediction을 앵커에 아주 작게 반영하는 방식이 개선을 만들었습니다.

가장 중요한 최신 전환점은 `a121`과 `a122`입니다.

- `a121`: `a117_09`의 high-error scenario를 다시 분석해 late slot, pack pressure, pack utilization, future stress 구간에서 구조적 과소예측이 있음을 확인
- `a122`: 위 신호를 바탕으로 `a117_09`를 유지하되 stress risk가 높은 일부 구간에만 작은 양수 uplift를 적용해 `10.0967991272` 달성

즉 현재 방향은 새 backbone을 무작정 키우는 것이 아니라, public에서 검증된 앵커가 구조적으로 틀리는 구간을 찾아 아주 제한적으로 보정하는 것입니다.

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
| a122 | `10.0967991272` | late/high-stress 과소예측 구간에 small uplift 적용 |

## 문서 구성

- [프로젝트 개요](docs/project_overview.md)
- [실험 로그](docs/experiment_log.md)
- [일일 리포트](docs/daily_report.md)
- [날짜별 작업 기록](docs/daily_logs/)
- [public 점수 로그](docs/public_score_log.json)
