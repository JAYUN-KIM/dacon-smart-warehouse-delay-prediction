# 실험 로그

## 현재 최고 기록

- 최고 제출: `submission_a124_1443.csv`
- Public MAE: `10.0960054075`
- 기준일: `2026-04-29`
- 핵심 방향: late/high-stress 구간에서 평균 지연을 보존하면서 후반 슬롯 쪽으로 uplift를 재배치하는 방식

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
| a124 | `submission_a124_1443.csv` | 10.0960054075 | late-shift mean-preserving uplift로 새 최고점 |

## 2026-04-29 실험 요약

### a123

- 제출: `submission_a123_059.csv`
- Public MAE: `10.0967996581`
- 목적: a122 기반 stress tail two-tier 보정
- 결과: a122와 거의 동일하나 `0.0000005309` 정도 소폭 악화
- 해석: stress tail을 더 강하게 더하는 방식은 안전한 개선축이 아니었다.

### a124

- 제출: `submission_a124_1443.csv`
- Public MAE: `10.0960054075`
- 후보명: `mean_late_q0.900_m0.055_f0.45_s12_d8_p0.75`
- family: `mean_preserving_late_shift`
- OOF MAE: `7.764461517333984`
- test mean uplift: `0.055000`
- test max uplift: `0.883358`
- coverage: `0.10000`
- a122 대비 test L1 변화량: `0.015619`

해석:

- a123처럼 stress tail을 단순히 더 키우는 것은 먹히지 않았다.
- a124는 평균 uplift를 유지하면서 후반 슬롯으로 보정량을 옮겼고, 이 방식은 public에서 새 최고점을 만들었다.
- 현재 병목은 "어떤 샘플을 크게 올릴까"보다 "언제, 어느 슬롯으로, 얼마나 부드럽게 이동시킬까"에 더 가깝다.

## 다음 실험 방향

2026-04-30에는 `a125`부터 시작한다.

- a124_1443을 anchor로 둔다.
- `q=0.900`, `target_mean=0.055`, `floor=0.45`, `start=12`, `denom=8`, `power=0.75` 주변을 세밀하게 탐색한다.
- mean uplift는 `0.052~0.058`, coverage는 `0.095~0.105`, max uplift는 `0.80~0.90` 안에서 먼저 제한한다.
- public-safe 후보와 aggressive 후보를 분리해서 제출 리스크를 관리한다.

## 현재 결론

9점대 진입을 위해 완전히 새로운 모델을 무작정 갈아타기보다, 현재 public이 반응한 late/high-stress underprediction 보정축을 더 정밀하게 다듬는 것이 우선이다. 단, correction을 강하게 추가하는 방식은 반복적으로 실패했으므로, `a124`처럼 평균을 보존하고 slot profile을 재배치하는 부드러운 형태가 더 유망하다.
