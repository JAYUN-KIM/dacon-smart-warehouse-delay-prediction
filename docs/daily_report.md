# 일일 리포트

- 작성 날짜: `2026-05-03`
- 현재 최고 public 점수: `10.010757563`
- 현재 최고 제출 파일: `submission_a145_4830.csv`
- 다음 작업: `a149` 후보 제출 및 9점대 진입 도박

## 오늘의 변화

오늘은 10.02대에서 10.01 초반까지 크게 전진한 날입니다. 전날 `a138_147`의 public `10.0265043299`에서 시작해, 기존 미세조정 축을 버리고 더 공격적인 미래 압력 기반 슬롯 재분배를 밀었습니다.

처음에는 tail expert와 공격적 후보를 넓게 테스트했고, `submission_a139_511.csv`가 public `10.0208783095`를 기록했습니다. 이후 단순 tail 강화만으로는 9점대까지 부족하다고 판단해, scenario 평균은 보존하면서 같은 scenario 안의 25개 슬롯 예측값을 미래 압력 신호에 맞춰 재분배하는 방향으로 전환했습니다.

이 전환이 오늘의 핵심이었습니다. `a145` 계열에서 `submission_a145_1755.csv`가 public `10.0143960347`을 기록했고, 더 공격적인 `submission_a145_4830.csv`가 public `10.010757563`까지 내려가며 현재 최고 기록을 세웠습니다.

## 오늘 확인한 public 점수

| 제출 | public MAE | 해석 |
| --- | ---: | --- |
| `submission_a139_511.csv` | `10.0208783095` | 공격적 tail expert 계열로 전날 best 대비 추가 개선 |
| `submission_a141_014.csv` | `10.0255310477` | 장시간 후보였지만 public에서는 후퇴 |
| `submission_a145_1755.csv` | `10.0143960347` | future-pressure slot redistribution 축이 강하게 적중 |
| `submission_a145_4830.csv` | `10.010757563` | 현재 최고 기록, 9점대 직전까지 접근 |

## 오늘의 실험 요약

### a139: 공격적 tail expert

- 목적: 기존 raw-only reboot family 위에서 high-delay tail을 더 강하게 밀어 public 개선을 만드는 것
- 결과: `submission_a139_511.csv`가 `10.0208783095`를 기록
- 판단: 방향은 유효했지만, 단순 tail 강화만으로는 9점대 돌파력이 부족했습니다.

### a142/a143: retrieval/layout residual 재시도

- 목적: scenario retrieval 또는 layout residual transfer를 통해 기존 축과 다른 일반화 신호를 찾는 것
- 판단: 오늘 최고 기록을 만드는 핵심 축은 아니었습니다.
- 결론: retrieval/layout residual보다 미래 운영 압력과 슬롯별 분배가 더 강한 신호였습니다.

### a144/a145: future-pressure slot redistribution

- 목적: scenario 평균은 보존하되, 25개 슬롯 안에서 미래 압력과 출고 지연 가능성이 큰 구간으로 예측 질량을 재분배
- 핵심 아이디어: public에서 계속 관찰된 underprediction이 단순 평균 문제가 아니라 슬롯 위치 문제일 수 있다고 보고, 같은 scenario 안의 rank/pressure profile을 조절
- 결과:
  - `submission_a145_1755.csv`: `10.0143960347`
  - `submission_a145_4830.csv`: `10.010757563`
- 판단: 오늘의 가장 큰 breakthrough입니다.

### a146/a147/a148/a149: 다음 도박 후보 탐색

- `a146`: horizon/rank rewire 실험. 방향 확인용으로는 의미 있었지만 `a145_4830`을 넘는 public 후보로 확신하기는 어려웠습니다.
- `a147`: scenario-level bias reboot. scenario residual model의 상관은 있었지만 최종 MAE 개선으로 이어지지 않아 보류했습니다.
- `a148`: public-guided interpolation으로 `a145_4830` 성공 후보를 재확인했습니다.
- `a149`: `a145_4830`을 anchor로 두고 9점대 진입을 위한 extrapolation 후보를 생성했습니다.

## 다음 제출 후보

| 후보 | 성격 | OOF MAE | p99 | max | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| `submission_a149_085.csv` | 안전 | `8.5729619473` | `50.1012` | `66.1678` | 안정적이지만 9점대 돌파력은 약할 수 있음 |
| `submission_a149_008.csv` | 균형 잡힌 공격 | `8.5718791547` | `50.3072` | `66.3585` | 다음 1순위 제출 후보 |
| `submission_a149_009.csv` | 강한 도박 | `8.5715741606` | `50.4171` | `66.4545` | 제출 기회가 남으면 공격적으로 시도할 후보 |

## 오늘의 결론

1. 10.09대 이후 미세조정 축은 개선 폭이 너무 작았습니다.
2. raw-only reboot와 대규모 미래창/도메인 피처 확장이 큰 점프를 만들었습니다.
3. 오늘의 결정적 개선은 `future-pressure slot redistribution`에서 나왔습니다.
4. 현재 best는 `submission_a145_4830.csv`의 `10.010757563`입니다.
5. 12시 이후에는 `a149_008`을 1순위로, 필요하면 `a149_009`를 9점대 도박 카드로 제출하는 전략이 가장 합리적입니다.

## 한 줄 요약

오늘은 기존 미세조정에서 벗어나 미래 압력 기반 슬롯 재분배라는 새 축을 찾았고, public `10.010757563`까지 도달했습니다. 이제 다음 목표는 같은 축을 더 공격적으로 밀어 9점대 문턱을 넘는 것입니다.
